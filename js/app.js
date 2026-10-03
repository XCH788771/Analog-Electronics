/**
 * 模拟电子技术课程网站主应用逻辑
 */

// 应用状态
const appState = {
    currentModule: 'learning',      // 当前模块: learning, training, testing
    currentView: 'chapter',         // 当前视图: chapter, graph
    currentChapter: null,           // 当前选中的章节
    currentSection: null,           // 当前选中的小节
    expandedChapters: new Set(),    // 展开的章节
    filters: {
        types: new Set(),           // 选中的问题类型
        objectives: new Set()       // 选中的教学目标
    },
    graph: {
        scale: 1,
        translateX: 0,
        translateY: 0,
        isDragging: false,
        startX: 0,
        startY: 0
    }
};

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', function() {
    initChapterTree();
    initModuleTabs();
    initViewToggle();
    initFilters();
    initGraphView();
    renderWelcomePage();
});

// ==================== 模块切换 ====================
function initModuleTabs() {
    const tabs = document.querySelectorAll('.module-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const module = tab.dataset.module;
            switchModule(module);
        });
    });
}

function switchModule(module) {
    appState.currentModule = module;
    
    // 更新标签状态
    document.querySelectorAll('.module-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.module === module);
    });
    
    // 更新内容
    if (appState.currentSection) {
        renderSectionContent(appState.currentSection);
    } else {
        renderWelcomePage();
    }
    
    updateContentHeader();
}

// ==================== 视图切换 ====================
function initViewToggle() {
    const btns = document.querySelectorAll('.view-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });
}

function switchView(view) {
    appState.currentView = view;
    
    // 更新按钮状态
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });
    
    // 切换侧边栏和内容区
    const sidebar = document.querySelector('.sidebar');
    const contentArea = document.querySelector('.content-area');
    
    if (view === 'chapter') {
        sidebar.style.display = 'flex';
        contentArea.innerHTML = getContentAreaHTML();
        if (appState.currentSection) {
            renderSectionContent(appState.currentSection);
        } else {
            renderWelcomePage();
        }
    } else if (view === 'focus') {
        sidebar.style.display = 'none';
        renderFocusView();
    } else {
        sidebar.style.display = 'none';
        renderGraphView();
    }
    
    updateContentHeader();
}

function getContentAreaHTML() {
    return `
        <div class="content-header">
            <div class="breadcrumb" id="breadcrumb">
                <span class="breadcrumb-item">首页</span>
            </div>
            <div class="content-actions">
                <button class="btn" onclick="toggleSidebar()">
                    <span>☰</span>
                </button>
            </div>
        </div>
        <div class="content-body" id="contentBody"></div>
    `;
}

// ==================== 章节树 ====================
function initChapterTree() {
    const treeContainer = document.getElementById('chapterTree');
    
    courseData.chapters.forEach((chapter, index) => {
        const chapterEl = createChapterElement(chapter, index);
        treeContainer.appendChild(chapterEl);
    });
    
    // 添加实验部分
    const experimentsSection = createExperimentsSection();
    treeContainer.appendChild(experimentsSection);
}

function createChapterElement(chapter, index) {
    const div = document.createElement('div');
    div.className = 'chapter-item';
    div.dataset.chapterId = chapter.id;
    
    // 默认展开第一章
    if (index === 0) {
        div.classList.add('expanded');
        appState.expandedChapters.add(chapter.id);
    }
    
    const validSections = chapter.sections.filter(s => !s.omitted);
    
    div.innerHTML = `
        <div class="chapter-header">
            <span class="arrow">▶</span>
            <span class="chapter-number">${chapter.number}</span>
            <span class="chapter-title">${chapter.title}</span>
            <span class="chapter-badge">${validSections.length}</span>
        </div>
        <div class="section-list"></div>
    `;
    
    // 章节点击展开/收起
    div.querySelector('.chapter-header').addEventListener('click', (e) => {
        e.stopPropagation();
        toggleChapter(chapter.id);
    });
    
    // 生成小节列表
    const sectionList = div.querySelector('.section-list');
    chapter.sections.forEach(section => {
        const sectionEl = createSectionElement(section, chapter);
        sectionList.appendChild(sectionEl);
        
        // 添加子章节列表（如果有）
        const subList = createSubsectionList(section, chapter);
        if (subList) {
            sectionList.appendChild(subList);
        }
    });
    
    return div;
}

function createSectionElement(section, chapter) {
    const div = document.createElement('div');
    div.className = 'section-item';
    div.dataset.sectionId = section.id;
    
    if (section.omitted) div.classList.add('omitted');
    if (section.selfStudy) div.classList.add('self-study');
    if (section.subsections) div.classList.add('has-subsections');
    
    // 标签点
    const types = section.types || [];
    const tagDots = types.map(type => {
        const typeInfo = Object.values(QUESTION_TYPES).find(t => t.id === type);
        return `<span class="tag-dot" style="background: ${typeInfo ? typeInfo.color : '#ccc'}" title="${typeInfo ? typeInfo.name : ''}"></span>`;
    }).join('');
    
    let icon = '📄';
    if (section.selfStudy) icon = '📖';
    if (section.omitted) icon = '🚫';
    
    div.innerHTML = `
        ${section.subsections ? '<span class="section-icon">▶</span>' : ''}
        <span class="section-icon">${icon}</span>
        <span class="section-title">${section.title}</span>
        <span class="section-tags">${tagDots}</span>
    `;
    
    // 点击事件
    div.addEventListener('click', (e) => {
        e.stopPropagation();
        if (section.subsections) {
            div.classList.toggle('expanded');
        }
        selectSection(section, chapter);
    });
    
    return div;
}

function createSubsectionList(section, chapter) {
    if (!section.subsections) return null;
    
    const subList = document.createElement('div');
    subList.className = 'subsection-list';
    section.subsections.forEach(sub => {
        const subEl = document.createElement('div');
        subEl.className = 'subsection-item';
        subEl.dataset.sectionId = sub.id;
        subEl.textContent = sub.title;
        subEl.addEventListener('click', (e) => {
            e.stopPropagation();
            selectSection(sub, chapter);
        });
        subList.appendChild(subEl);
    });
    return subList;
}

function createExperimentsSection() {
    const div = document.createElement('div');
    div.className = 'experiments-section';
    div.innerHTML = `
        <div class="experiments-title">
            <span>🧪</span>
            <span>实验课程</span>
        </div>
    `;
    
    courseData.experiments.forEach(exp => {
        const expEl = document.createElement('div');
        expEl.className = 'experiment-item';
        expEl.dataset.expId = exp.id;
        expEl.innerHTML = `
            <span>🔬</span>
            <span>${exp.title}</span>
        `;
        expEl.addEventListener('click', () => selectExperiment(exp));
        div.appendChild(expEl);
    });
    
    return div;
}

function toggleChapter(chapterId) {
    const chapterEl = document.querySelector(`.chapter-item[data-chapter-id="${chapterId}"]`);
    if (chapterEl) {
        chapterEl.classList.toggle('expanded');
        if (appState.expandedChapters.has(chapterId)) {
            appState.expandedChapters.delete(chapterId);
        } else {
            appState.expandedChapters.add(chapterId);
        }
    }
}

function selectSection(section, chapter) {
    appState.currentSection = section;
    appState.currentChapter = chapter;
    
    // 更新选中状态
    document.querySelectorAll('.section-item, .subsection-item, .experiment-item').forEach(el => {
        el.classList.remove('active');
    });
    
    const sectionEl = document.querySelector(`[data-section-id="${section.id}"]`);
    if (sectionEl) sectionEl.classList.add('active');
    
    // 渲染内容
    renderSectionContent(section);
    updateContentHeader();
}

function selectExperiment(experiment) {
    appState.currentSection = experiment;
    appState.currentChapter = { id: experiment.chapter, title: '实验课程' };
    
    // 更新选中状态
    document.querySelectorAll('.section-item, .subsection-item, .experiment-item').forEach(el => {
        el.classList.remove('active');
    });
    
    const expEl = document.querySelector(`[data-exp-id="${experiment.id}"]`);
    if (expEl) expEl.classList.add('active');
    
    // 渲染内容
    renderExperimentContent(experiment);
    updateContentHeader();
}

// ==================== 筛选功能 ====================
function initFilters() {
    // 问题类型筛选
    const typeFilters = document.getElementById('typeFilters');
    Object.values(QUESTION_TYPES).forEach(type => {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.dataset.filterType = 'type';
        chip.dataset.filterValue = type.id;
        chip.innerHTML = `<span class="dot" style="background: ${type.color}"></span>${type.name}`;
        chip.addEventListener('click', () => toggleFilter('types', type.id, chip));
        typeFilters.appendChild(chip);
    });
    
    // 教学目标筛选
    const objectiveFilters = document.getElementById('objectiveFilters');
    Object.values(LEARNING_OBJECTIVES).forEach(obj => {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.dataset.filterType = 'objective';
        chip.dataset.filterValue = obj.id;
        chip.innerHTML = `<span class="dot" style="background: ${obj.color}"></span>${obj.name}`;
        chip.addEventListener('click', () => toggleFilter('objectives', obj.id, chip));
        objectiveFilters.appendChild(chip);
    });
}

function toggleFilter(filterGroup, value, element) {
    const set = appState.filters[filterGroup];
    if (set.has(value)) {
        set.delete(value);
        element.classList.remove('active');
    } else {
        set.add(value);
        element.classList.add('active');
    }
    
    applyFilters();
}

function applyFilters() {
    const { types, objectives } = appState.filters;
    
    // 遍历所有章节和小节
    courseData.chapters.forEach(chapter => {
        const chapterEl = document.querySelector(`.chapter-item[data-chapter-id="${chapter.id}"]`);
        if (!chapterEl) return;
        
        let chapterVisible = false;
        
        chapter.sections.forEach(section => {
            const sectionEl = document.querySelector(`.section-item[data-section-id="${section.id}"]`);
            if (!sectionEl) return;
            
            let visible = true;
            const sectionTypes = section.types || [];
            const sectionObjectives = section.objectives || [];
            
            // 检查类型筛选
            if (types.size > 0) {
                visible = sectionTypes.some(t => types.has(t));
            }
            
            // 检查目标筛选
            if (visible && objectives.size > 0) {
                visible = sectionObjectives.some(o => objectives.has(o));
            }
            
            sectionEl.style.display = visible ? 'flex' : 'none';
            if (visible) chapterVisible = true;
            
            // 子章节
            if (section.subsections) {
                section.subsections.forEach(sub => {
                    const subEl = document.querySelector(`.subsection-item[data-section-id="${sub.id}"]`);
                    if (!subEl) return;
                    
                    let subVisible = true;
                    if (types.size > 0) {
                        subVisible = sub.types.some(t => types.has(t));
                    }
                    if (subVisible && objectives.size > 0) {
                        subVisible = sub.objectives.some(o => objectives.has(o));
                    }
                    
                    subEl.style.display = subVisible ? 'block' : 'none';
                    if (subVisible) chapterVisible = true;
                });
            }
        });
        
        chapterEl.style.display = chapterVisible ? 'block' : 'none';
    });
    
    // 实验筛选
    const expItems = document.querySelectorAll('.experiment-item');
    expItems.forEach(item => {
        const expId = item.dataset.expId;
        const exp = courseData.experiments.find(e => e.id === expId);
        if (!exp) return;
        
        let visible = true;
        if (types.size > 0) {
            visible = exp.types.some(t => types.has(t));
        }
        if (visible && objectives.size > 0) {
            visible = exp.objectives.some(o => objectives.has(o));
        }
        
        item.style.display = visible ? 'flex' : 'none';
    });
}

// ==================== 内容渲染 ====================
function renderWelcomePage() {
    const contentBody = document.getElementById('contentBody');
    if (!contentBody) return;
    
    const moduleInfo = RESOURCE_MODULES[appState.currentModule.toUpperCase()];
    
    // 统计数据
    let totalSections = 0;
    let totalChapters = courseData.chapters.length;
    let totalExperiments = courseData.experiments.length;
    
    courseData.chapters.forEach(ch => {
        ch.sections.forEach(s => {
            if (!s.omitted) totalSections++;
            if (s.subsections) totalSections += s.subsections.length;
        });
    });
    
    // 游戏闯关卡片（样式与重点难点卡片一致）
    const gameCards = GAME_TOPICS.map(g => {
        const circuit = g.circuitId ? CORE_CIRCUITS.find(c => c.id === g.circuitId) : null;
        const color = circuit ? circuit.color : (g.color || '#64748b');
        const icon = circuit ? circuit.icon : (g.icon || '🎮');
        return `
            <div class="home-core-card" onclick="openTopicPage('game', '${g.circuitId || 'regulator'}')" style="--card-color: ${color};">
                <div class="home-core-icon" style="background: ${color}15; color: ${color};">${icon}</div>
                <div class="home-core-info">
                    <h4>${g.name}</h4>
                    <p class="home-core-desc">${(CIRCUIT_BRANCHES[g.circuitId || 'regulator'] || []).length} 种电路 · 点击进入闯关</p>
                </div>
                <div class="home-core-arrow">→</div>
            </div>
        `;
    }).join('');
    
    // 题型分类
    const calcTopics = QUESTION_TYPE_TOPICS.calculation.map(item => {
        const circuit = item.circuitId ? CORE_CIRCUITS.find(c => c.id === item.circuitId) : null;
        const color = circuit ? circuit.color : (item.color || '#64748b');
        const icon = circuit ? circuit.icon : (item.icon || '📌');
        const onClick = `openTopicPage('qtype', '${item.circuitId || 'regulator'}')`;
        return `<div class="home-q-item-card" onclick="${onClick}" style="--qcard-color: ${color};">
            <div class="home-q-item-icon" style="background: ${color}15; color: ${color};">${icon}</div>
            <span>${item.name}</span>
        </div>`;
    }).join('');
    
    const designTopics = QUESTION_TYPE_TOPICS.design.map(item => {
        const circuit = item.circuitId ? CORE_CIRCUITS.find(c => c.id === item.circuitId) : null;
        const color = circuit ? circuit.color : (item.color || '#64748b');
        const icon = circuit ? circuit.icon : (item.icon || '📌');
        const onClick = `openTopicPage('qtype', '${item.circuitId || 'regulator'}')`;
        return `<div class="home-q-item-card" onclick="${onClick}" style="--qcard-color: ${color};">
            <div class="home-q-item-icon" style="background: ${color}15; color: ${color};">${icon}</div>
            <span>${item.name}</span>
        </div>`;
    }).join('');
    
    contentBody.innerHTML = `
        <div class="home-page">
            <!-- Hero 区域 -->
            <div class="home-hero">
                <div class="home-hero-content">
                    <div class="home-hero-badge">INTERACTIVE LEARNING</div>
                    <h1 class="home-hero-title">${courseData.title}</h1>
                    <p class="home-hero-subtitle">${courseData.subtitle} · 交互式教学资源平台</p>
                    <div class="home-hero-stats">
                        <div class="home-hero-stat">
                            <span class="stat-num">${totalChapters}</span>
                            <span class="stat-label">章节</span>
                        </div>
                        <div class="home-hero-divider"></div>
                        <div class="home-hero-stat">
                            <span class="stat-num">${totalSections}</span>
                            <span class="stat-label">知识点</span>
                        </div>
                        <div class="home-hero-divider"></div>
                        <div class="home-hero-stat">
                            <span class="stat-num">${totalExperiments}</span>
                            <span class="stat-label">实验</span>
                        </div>
                        <div class="home-hero-divider"></div>
                        <div class="home-hero-stat">
                            <span class="stat-num">5</span>
                            <span class="stat-label">核心电路</span>
                        </div>
                    </div>
                </div>
                <div class="home-hero-deco">
                    <div class="deco-circle deco-1"></div>
                    <div class="deco-circle deco-2"></div>
                    <div class="deco-circle deco-3"></div>
                </div>
            </div>
            
            <!-- 课程资源区 -->
            <div class="home-section">
                <div class="home-section-header">
                    <h3 class="home-section-title">📦 课程资源</h3>
                    <span class="home-section-desc">系统化的学习、训练与测试资源</span>
                </div>
                <div class="home-modules-grid">
                    <div class="home-module-card learning" onclick="openLearningResources()">
                        <div class="home-module-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                            </svg>
                        </div>
                        <div class="home-module-info">
                            <h4>学习资源</h4>
                            <p>课件 · 视频 · 动画 · 仿真</p>
                        </div>
                        <div class="home-module-arrow">→</div>
                    </div>
                    <div class="home-module-card training" onclick="switchModule('training')">
                        <div class="home-module-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 20h9"/>
                                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
                            </svg>
                        </div>
                        <div class="home-module-info">
                            <h4>训练资源</h4>
                            <p>例题 · 习题 · 练习 · 考研</p>
                        </div>
                        <div class="home-module-arrow">→</div>
                    </div>
                    <div class="home-module-card testing" onclick="switchModule('testing')">
                        <div class="home-module-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M9 11l3 3L22 4"/>
                                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                            </svg>
                        </div>
                        <div class="home-module-info">
                            <h4>测试资源</h4>
                            <p>测验 · 考核 · 设计评估</p>
                        </div>
                        <div class="home-module-arrow">→</div>
                    </div>
                </div>
            </div>
            
            <!-- 游戏闯关区 -->
            <div class="home-section">
                <div class="home-section-header">
                    <h3 class="home-section-title">🎮 游戏闯关</h3>
                    <span class="home-section-desc">以游戏方式闯关各电路知识</span>
                </div>
                <div class="home-game-grid">
                    ${gameCards}
                </div>
            </div>

            <!-- 题型解析区 -->
            <div class="home-section">
                <div class="home-section-header">
                    <h3 class="home-section-title">📝 题型解析</h3>
                    <span class="home-section-desc">按题型快速定位练习内容</span>
                </div>
                <div class="home-qtype-grid">
                    <div class="home-qtype-card calc">
                        <div class="home-qtype-header">
                            <div class="home-qtype-icon calc-icon">🧮</div>
                            <h4>计算题</h4>
                            <span class="home-qtype-count">${QUESTION_TYPE_TOPICS.calculation.length} 类</span>
                        </div>
                        <div class="home-qtype-list">
                            ${calcTopics}
                        </div>
                    </div>
                    <div class="home-qtype-card design">
                        <div class="home-qtype-header">
                            <div class="home-qtype-icon design-icon">🎨</div>
                            <h4>设计题</h4>
                            <span class="home-qtype-count">${QUESTION_TYPE_TOPICS.design.length} 类</span>
                        </div>
                        <div class="home-qtype-list">
                            ${designTopics}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ==================== 学习资源页（重点难点 + 其它知识点） ====================
// 五大核心电路卡片（原首页重点难点模块，现挂在学习资源页）
function buildCoreCircuitCards() {
    return CORE_CIRCUITS.map(circuit => {
        const badges = [];
        if (circuit.isKey) badges.push('<span class="home-badge key-badge">重点</span>');
        if (circuit.isDifficult) badges.push('<span class="home-badge diff-badge">难点</span>');
        return `
            <div class="home-core-card" onclick="goToCoreCircuit('${circuit.id}')" style="--card-color: ${circuit.color};">
                <div class="home-core-icon" style="background: ${circuit.color}15; color: ${circuit.color};">${circuit.icon}</div>
                <div class="home-core-info">
                    <h4>${circuit.name}</h4>
                    <div class="home-core-badges">${badges.join('')}</div>
                </div>
                <div class="home-core-arrow">→</div>
            </div>
        `;
    }).join('');
}

function openLearningResources() {
    appState.currentSection = null;
    switchView('chapter');
    renderLearningResPage();
}

function renderLearningResPage() {
    const contentBody = document.getElementById('contentBody');
    if (!contentBody) return;

    // 其它知识点：除五大核心电路关联标签外的章节/知识体系知识点
    const coreIds = new Set();
    CORE_CIRCUITS.forEach(c => c.tagIds.forEach(id => coreIds.add(id)));
    const otherTags = KNOWLEDGE_TAGS.filter(t => (t.type === 'section' || t.type === 'topic') && !coreIds.has(t.id));
    const otherCards = otherTags.map(t => {
        const color = t.category === 'chapter' ? '#3b82f6' : '#8b5cf6';
        const icon = t.category === 'chapter' ? '📖' : '🧩';
        return `
            <div class="home-core-card" onclick="navigateToSection('${t.id}')" style="--card-color: ${color};">
                <div class="home-core-icon" style="background: ${color}15; color: ${color};">${icon}</div>
                <div class="home-core-info">
                    <h4>${t.name}</h4>
                    <p class="home-core-desc">${t.category === 'chapter' ? '章节知识点' : '知识体系知识点'}</p>
                </div>
                <div class="home-core-arrow">→</div>
            </div>
        `;
    }).join('');

    contentBody.innerHTML = `
        <div class="home-page">
            <div class="home-hero">
                <div class="home-hero-content">
                    <div class="home-hero-badge">INTERACTIVE LEARNING</div>
                    <h1 class="home-hero-title">交互式学习资源</h1>
                    <p class="home-hero-subtitle">重点难点逐一攻克 · 其它知识点系统覆盖</p>
                    <div style="margin-top: 16px;">
                        <button class="btn" onclick="renderWelcomePage()">
                            <span>←</span>
                            <span>返回首页</span>
                        </button>
                    </div>
                </div>
            </div>

            <div class="home-section">
                <div class="home-section-header">
                    <h3 class="home-section-title">🎯 重点难点</h3>
                    <span class="home-section-desc">五大核心放大电路，课程精华所在</span>
                </div>
                <div class="home-core-grid">
                    ${buildCoreCircuitCards()}
                </div>
            </div>

            <div class="home-section">
                <div class="home-section-header">
                    <h3 class="home-section-title">📚 其它知识点</h3>
                    <span class="home-section-desc">除五大核心电路外的章节与知识体系知识点（${otherTags.length} 个）</span>
                </div>
                <div class="home-core-grid">
                    ${otherCards}
                </div>
            </div>
        </div>
    `;
    contentBody.scrollTop = 0;
}

// ==================== 交互式电路界面（16:9 弹窗） ====================
function openCircuitLab(src) {
    // 避免重复打开
    closeCircuitLab();
    const overlay = document.createElement('div');
    overlay.className = 'circuit-lab-overlay';
    overlay.id = 'circuitLabOverlay';
    overlay.innerHTML = `<iframe src="${src}" title="交互式电路"></iframe>`;
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeCircuitLab();
    });
    document.body.appendChild(overlay);
}

function closeCircuitLab() {
    const old = document.getElementById('circuitLabOverlay');
    if (old) old.remove();
}

// 接收交互页面内关闭/返回按钮的消息（两者均移除弹窗；返回后即回到打开电路的上一级专题页面）
window.addEventListener('message', (e) => {
    if (e.data && (e.data.type === 'close-circuit-lab' || e.data.type === 'back-circuit-lab')) closeCircuitLab();
});

// 跳转到核心电路详情（学习资源）
function goToCoreCircuit(circuitId) {
    switchView('focus');
    appState.focusCategory = 'core_circuits';
    appState.selectedCircuit = circuitId;
    setTimeout(() => renderFocusCategory('core_circuits', circuitId), 50);
}

// ==================== 专题导航 ====================
appState.focusCategory = null;

function renderFocusView() {
    const contentArea = document.querySelector('.content-area');
    
    if (appState.focusCategory) {
        renderFocusCategory(appState.focusCategory);
        return;
    }
    
    // 专题导航首页
    const moduleInfo = RESOURCE_MODULES[appState.currentModule.toUpperCase()];
    
    const categoryCards = FOCUS_CATEGORIES.map(cat => {
        const tags = getTagsByFocusCategory(cat.id);
        return `
            <div class="focus-cat-card" onclick="selectFocusCategory('${cat.id}')" style="--cat-color: ${cat.color};">
                <div class="focus-cat-icon" style="background: ${cat.color}20; color: ${cat.color};">${cat.icon}</div>
                <div class="focus-cat-info">
                    <h3>${cat.name}</h3>
                    <p>${cat.description}</p>
                    <span class="focus-cat-count">${tags.length} 个知识点</span>
                </div>
            </div>
        `;
    }).join('');
    
    // 五大核心电路快捷入口
    const circuitCards = CORE_CIRCUITS.map(circuit => `
        <div class="core-circuit-card" onclick="selectCoreCircuit('${circuit.id}')" style="--circuit-color: ${circuit.color};">
            <div class="circuit-icon" style="background: ${circuit.color}20; color: ${circuit.color};">${circuit.icon}</div>
            <div class="circuit-info">
                <h4>${circuit.name}</h4>
                <p>${circuit.description}</p>
                <div class="circuit-tags">
                    ${circuit.questionTypes.map(t => {
                        const qt = Object.values(QUESTION_TYPES).find(q => q.id === t);
                        return qt ? `<span class="mini-tag" style="background: ${qt.color}20; color: ${qt.color};">${qt.name}</span>` : '';
                    }).join('')}
                    ${circuit.designFocus ? '<span class="mini-tag design-tag">设计重点</span>' : ''}
                </div>
            </div>
        </div>
    `).join('');
    
    contentArea.innerHTML = `
        <div class="content-header">
            <div class="breadcrumb" id="breadcrumb">
                <span class="breadcrumb-item">专题导航</span>
            </div>
            <div class="content-actions">
                <button class="btn" onclick="switchView('chapter')">
                    <span>📖</span>
                    <span>课程导航</span>
                </button>
            </div>
        </div>
        <div class="content-body" id="contentBody">
            <div class="focus-view">
                <div class="focus-hero">
                    <h2>专题导航</h2>
                    <p>按知识类型浏览课程内容 · 当前模块：${moduleInfo.name}</p>
                </div>
                
                <div class="focus-section">
                    <h3 class="focus-section-title">⚡ 五大核心放大电路</h3>
                    <p class="focus-section-desc">模电核心内容，计算题和设计题的主要考察对象</p>
                    <div class="core-circuits-grid">${circuitCards}</div>
                </div>
                
                <div class="focus-section">
                    <h3 class="focus-section-title">📋 分类导航</h3>
                    <p class="focus-section-desc">按内容属性和题型分类，快速定位相关知识点</p>
                    <div class="focus-cat-grid">${categoryCards}</div>
                </div>
            </div>
        </div>
    `;
}

function selectFocusCategory(categoryId) {
    appState.focusCategory = categoryId;
    renderFocusCategory(categoryId);
}

function selectCoreCircuit(circuitId) {
    appState.focusCategory = 'core_circuits';
    appState.selectedCircuit = circuitId;
    renderFocusCategory('core_circuits', circuitId);
}

// ==================== 专题页（游戏闯关 / 题型解析） ====================
// 非核心电路的兜底信息（直流稳压电源等）
const REGULATOR_META = { id: 'regulator', name: '直流稳压电源', icon: '⚡', color: '#14b8a6', description: '整流、滤波与稳压电路', learning: [], training: [], questionTypes: ['design'] };

function getCircuitMeta(circuitId) {
    return CORE_CIRCUITS.find(c => c.id === circuitId) || (circuitId === 'regulator' ? REGULATOR_META : { id: circuitId, name: circuitId, icon: '📌', color: '#64748b', description: '', learning: [], training: [], questionTypes: [] });
}

function openTopicPage(mode, circuitId) {
    appState.topicMode = mode;           // 'game' 游戏闯关 | 'qtype' 题型解析
    appState.selectedCircuit = circuitId;
    appState.selectedBranch = null;
    appState.focusCategory = null;
    switchView('focus');
    setTimeout(() => renderTopicPage(), 50);
}

// 案例缩略图（深绿底 + 白色电路示意，与交互电路页风格一致）
function caseThumb(type) {
    const wire = 'stroke="#ffffff" stroke-width="2" fill="none"';
    const thin = 'stroke="#ffffff" stroke-width="1.7" fill="none"';
    const tri = '<polygon points="62,30 62,66 100,48" fill="none" stroke="#ffffff" stroke-width="2"/>';
    const out = `<line x1="100" y1="48" x2="140" y2="48" ${wire}/>`;
    const fb = `<path d="M132 48 V18 H104" ${thin}/><rect x="78" y="12" width="26" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M78 18 H62 V38" ${thin}/>`;
    let inner = '';
    switch (type) {
        case 'noninv':
            inner = `<circle cx="16" cy="48" r="7" fill="none" stroke="#ffffff" stroke-width="2"/><path d="M12 48 q4 -6 8 0 q4 6 8 0" ${thin}/><line x1="23" y1="48" x2="62" y2="48" ${wire}/><text x="50" y="42" fill="#ffffff" font-size="11">+</text>${tri}${out}${fb}<text x="48" y="66" fill="#ffffff" font-size="11">−</text>`;
            break;
        case 'inv':
            inner = `<circle cx="16" cy="40" r="7" fill="none" stroke="#ffffff" stroke-width="2"/><path d="M12 40 q4 -6 8 0 q4 6 8 0" ${thin}/><line x1="23" y1="40" x2="34" y2="40" ${wire}/><rect x="34" y="34" width="24" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><line x1="58" y1="40" x2="62" y2="40" ${wire}/><text x="50" y="32" fill="#ffffff" font-size="11">−</text><line x1="62" y1="58" x2="50" y2="58" ${thin}/><line x1="50" y1="58" x2="50" y2="66" ${thin}/><line x1="42" y1="66" x2="58" y2="66" ${thin}/><line x1="45" y1="71" x2="55" y2="71" ${thin}/><line x1="48" y1="76" x2="52" y2="76" ${thin}/><text x="44" y="52" fill="#ffffff" font-size="11">+</text>${tri}${out}${fb}`;
            break;
        case 'sum':
            inner = `<line x1="10" y1="34" x2="26" y2="34" ${wire}/><rect x="26" y="28" width="22" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M48 34 H56 V42 H62" ${thin}/><line x1="10" y1="60" x2="26" y2="60" ${wire}/><rect x="26" y="54" width="22" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M48 60 H56 V54 H62" ${thin}/><text x="50" y="40" fill="#ffffff" font-size="11">−</text>${tri}${out}<path d="M132 48 V18 H104" ${thin}/><rect x="78" y="12" width="26" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M78 18 H62 V30" ${thin}/>`;
            break;
        case 'diff':
            inner = `<line x1="10" y1="34" x2="26" y2="34" ${wire}/><rect x="26" y="28" width="22" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M48 34 H56 V42 H62" ${thin}/><line x1="10" y1="62" x2="30" y2="62" ${wire}/><rect x="30" y="56" width="22" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M52 62 H56 V54 H62" ${thin}/><text x="50" y="40" fill="#ffffff" font-size="11">−</text><text x="50" y="72" fill="#ffffff" font-size="11">+</text>${tri}${out}<path d="M132 48 V18 H104" ${thin}/><rect x="78" y="12" width="26" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M78 18 H62 V30" ${thin}/>`;
            break;
        case 'multi':
            inner = `<line x1="8" y1="48" x2="28" y2="48" ${wire}/><polygon points="28,32 28,64 56,48" fill="none" stroke="#ffffff" stroke-width="2"/><line x1="56" y1="48" x2="84" y2="48" ${wire}/><polygon points="84,32 84,64 112,48" fill="none" stroke="#ffffff" stroke-width="2"/><line x1="112" y1="48" x2="146" y2="48" ${wire}/><text x="42" y="76" fill="#ffffff" font-size="10">A1</text><text x="96" y="76" fill="#ffffff" font-size="10">A2</text>`;
            break;
        default:
            inner = `<line x1="10" y1="48" x2="34" y2="48" ${wire}/><rect x="34" y="42" width="22" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><line x1="56" y1="48" x2="62" y2="48" ${wire}/>${tri}${out}<path d="M132 48 V18 H104" ${thin}/><rect x="78" y="12" width="26" height="12" fill="none" stroke="#ffffff" stroke-width="1.7"/><path d="M78 18 H62 V38" ${thin}/>`;
    }
    return `<svg viewBox="0 0 160 96" preserveAspectRatio="xMidYMid meet" style="display:block;width:100%;height:100%;"><rect x="0" y="0" width="160" height="96" rx="8" fill="#0b3d22"/>${inner}</svg>`;
}

function renderTopicPage() {
    const contentArea = document.querySelector('.content-area');
    if (!contentArea) return;
    const mode = appState.topicMode === 'game' ? 'game' : 'qtype';
    const circuit = getCircuitMeta(appState.selectedCircuit);
    const branches = CIRCUIT_BRANCHES[circuit.id] || [];
    const caseKey = mode === 'game' ? 'game' : 'calculation';
    const themeColor = mode === 'game' ? '#8b5cf6' : '#e74c3c';
    const modeName = mode === 'game' ? '游戏闯关' : '题型解析';
    const regionName = mode === 'game' ? '闯关电路' : '计算题型';

    const branchCards = branches.length ? branches.map(b => {
        const cnt = (((b.cases && b.cases[caseKey]) || []) || []).filter(c => c.lab).length;
        return `
            <div class="home-core-card branch-card" data-branch="${b.id}" style="--card-color: ${themeColor};" onclick="showCaseModule('${b.id}')">
                <div class="home-core-icon" style="background: ${themeColor}15; color: ${themeColor};">${mode === 'game' ? '🎮' : '🧮'}</div>
                <div class="home-core-info">
                    <h4>${b.name}</h4>
                    <p class="home-core-desc">${b.desc}</p>
                </div>
                <span class="branch-count">${cnt ? cnt + ' 个案例' : '建设中'}</span>
            </div>
        `;
    }).join('') : '<div class="region-empty">该专题的分支内容建设中，后续补充</div>';

    const heroTags = mode === 'game'
        ? '<span class="mini-tag" style="background: rgba(139, 92, 246, 0.15); color: #8b5cf6;">游戏闯关</span>'
        : '<span class="mini-tag" style="background: rgba(231, 76, 60, 0.15); color: #e74c3c;">计算题型</span><span class="mini-tag" style="background: rgba(46, 204, 113, 0.15); color: #2ecc71;">设计题型</span>';

    contentArea.innerHTML = `
        <div class="content-header">
            <div class="breadcrumb" id="breadcrumb">
                <span class="breadcrumb-item" onclick="backToHomePage()">首页</span> > <span class="breadcrumb-item">${modeName}</span> > <span class="breadcrumb-item">${circuit.name}</span>
            </div>
            <div class="content-actions">
                <button class="btn" onclick="backToHomePage()">← 返回</button>
            </div>
        </div>
        <div class="content-body" id="contentBody">
            <div class="focus-detail-view" id="topicPage">
                <div class="focus-detail-hero" style="background: linear-gradient(135deg, ${circuit.color}15, ${circuit.color}05);">
                    <div class="focus-detail-icon" style="color: ${circuit.color};">${circuit.icon}</div>
                    <h2>${circuit.name}</h2>
                    <p>${circuit.description}</p>
                    <div class="focus-detail-tags">${heroTags}</div>
                </div>

                <div class="circuit-region region-calc">
                    <div class="circuit-region-title">
                        <span class="circuit-region-dot"></span>
                        <span>${regionName}</span>
                        <span class="circuit-region-count">${branches.length} 种电路</span>
                    </div>
                    <div class="home-core-grid core-grid-2">${branchCards}</div>
                </div>

                <!-- 案例模块插入位（点击分支电路时出现，位于计算题型与设计题型之间） -->
                <div id="caseSlot"></div>

                ${mode === 'qtype' ? `
                <div class="circuit-region region-design" id="designRegion">
                    <div class="circuit-region-title">
                        <span class="circuit-region-dot"></span>
                        <span>设计题型</span>
                        <span class="circuit-region-count">0 项</span>
                    </div>
                    <div class="region-empty">内容建设中，后续补充</div>
                </div>` : ''}

                <div class="topic-hint">${mode === 'game' ? '点击任意电路查看闯关案例，点击空白处收起' : '点击任意电路查看解析案例，点击空白处收起'}</div>
            </div>
        </div>
    `;
    contentArea.scrollTop = 0;
}

// 显示某分支电路的案例模块（插在计算题型与设计题型之间，设计题型随之下移）
function showCaseModule(branchId) {
    const circuit = getCircuitMeta(appState.selectedCircuit);
    const branches = CIRCUIT_BRANCHES[circuit.id] || [];
    const branch = branches.find(b => b.id === branchId);
    const slot = document.getElementById('caseSlot');
    if (!branch || !slot) return;

    const mode = appState.topicMode === 'game' ? 'game' : 'qtype';
    const caseKey = mode === 'game' ? 'game' : 'calculation';
    const caseTitle = mode === 'game' ? '闯关案例' : '计算题型解析案例';
    const themeColor = mode === 'game' ? '#8b5cf6' : '#e74c3c';
    const allCases = (branch.cases && branch.cases[caseKey]) || [];
    const cases = allCases.filter(c => c.lab);   // 只显示实际建设好的案例
    appState.selectedBranch = branchId;

    document.querySelectorAll('.branch-card').forEach(el => el.classList.toggle('active', el.dataset.branch === branchId));

    const caseCards = cases.length ? cases.map((c, i) => `
        <div class="case-card ${c.lab ? 'has-lab' : ''}" ${c.lab ? `onclick="event.stopPropagation();openCircuitLab('${c.lab}')"` : ''}>
            <div class="case-thumb">
                ${c.thumbImg
                    ? `<img src="${c.thumbImg}" alt="${c.name}页面预览" loading="lazy" style="display:block;width:100%;height:100%;object-fit:cover;">`
                    : caseThumb(branch.thumb || 'generic')}
                <span class="case-index">案例${i + 1}</span>
            </div>
            <div class="case-meta">
                <h5>${c.name}</h5>
                <p>${c.desc || ''}</p>
                <span class="case-state ${c.lab ? 'ready' : ''}">${c.lab ? '🔬 点击进入交互电路' : '🚧 建设中'}</span>
            </div>
        </div>
    `).join('') : `
        <div class="case-card placeholder">
            <div class="case-thumb">${caseThumb(branch.thumb || 'generic')}</div>
            <div class="case-meta">
                <h5>案例建设中</h5>
                <p>该电路的${mode === 'game' ? '闯关' : '解析'}案例正在制作中，敬请期待</p>
                <span class="case-state">🚧 建设中</span>
            </div>
        </div>`;

    slot.innerHTML = `
        <div class="case-module" style="--case-color: ${themeColor};">
            <div class="case-module-header">
                <span class="case-module-dot"></span>
                <span>${branch.name} · ${caseTitle}</span>
                <span class="case-module-count">${cases.length ? cases.length + ' 个' : '建设中'}</span>
                <span class="case-module-close" onclick="hideCaseModule()" title="收起">✕</span>
            </div>
            <div class="case-grid">${caseCards}</div>
        </div>
    `;
    slot.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideCaseModule() {
    const slot = document.getElementById('caseSlot');
    if (slot) slot.innerHTML = '';
    appState.selectedBranch = null;
    document.querySelectorAll('.branch-card').forEach(el => el.classList.remove('active'));
}

// 点击专题页空白处收起案例模块（点击 Esc 同样收起）
document.addEventListener('click', e => {
    const slot = document.getElementById('caseSlot');
    if (!slot || !slot.innerHTML.trim()) return;
    if (e.target.closest('.case-module') || e.target.closest('.branch-card')) return;
    hideCaseModule();
});
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') hideCaseModule();
});

// 返回课程导航首页
function backToHomePage() {
    appState.focusCategory = null;
    appState.selectedCircuit = null;
    appState.currentSection = null;
    switchView('chapter');
}

function renderFocusCategory(categoryId, circuitId) {
    const contentArea = document.querySelector('.content-area');
    const cat = FOCUS_CATEGORIES.find(c => c.id === categoryId);
    const moduleInfo = RESOURCE_MODULES[appState.currentModule.toUpperCase()];
    
    let breadcrumb = `<span class="breadcrumb-item" onclick="backToFocusHome()">专题导航</span>`;
    
    if (categoryId === 'core_circuits' && circuitId) {
        // 学习模式：只显示学习资源（游戏闯关/题型解析走 renderTopicPage 专题页）
        const circuit = getCircuitMeta(circuitId);
        breadcrumb = `<span class="breadcrumb-item" onclick="backToFocusHome()">交互式学习资源</span>`;
        breadcrumb += ` > <span class="breadcrumb-item">${circuit.name}</span>`;

        // 学习资源区域卡片（带 lab 的可打开 16:9 交互电路界面）
        const learningCards = (circuit.learning || []).map(item => `
            <div class="home-core-card ${item.lab ? 'has-lab' : ''}" style="--card-color: #3b82f6;" ${item.lab ? `onclick="openCircuitLab('${item.lab}')"` : ''}>
                <div class="home-core-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">${item.lab ? '🔬' : '📖'}</div>
                <div class="home-core-info">
                    <h4>${item.name}</h4>
                    <p class="home-core-desc">${item.desc}${item.lab ? '<span class="lab-hint">点击进入交互电路</span>' : ''}</p>
                </div>
                ${item.lab ? '<div class="home-core-arrow">→</div>' : ''}
            </div>
        `).join('');

        contentArea.innerHTML = `
            <div class="content-header">
                <div class="breadcrumb" id="breadcrumb">${breadcrumb}</div>
                <div class="content-actions">
                    <button class="btn" onclick="backToFocusHome()">← 返回</button>
                </div>
            </div>
            <div class="content-body" id="contentBody">
                <div class="focus-detail-view">
                    <div class="focus-detail-hero" style="background: linear-gradient(135deg, ${circuit.color}15, ${circuit.color}05);">
                        <div class="focus-detail-icon" style="color: ${circuit.color};">${circuit.icon}</div>
                        <h2>${circuit.name}</h2>
                        <p>${circuit.description}</p>
                        <div class="focus-detail-tags">
                            ${circuit.questionTypes.map(t => {
                                const qt = Object.values(QUESTION_TYPES).find(q => q.id === t);
                                return qt ? `<span class="mini-tag" style="background: ${qt.color}20; color: ${qt.color};">${qt.name}</span>` : '';
                            }).join('')}
                            ${circuit.designFocus ? '<span class="mini-tag design-tag">设计重点</span>' : ''}
                        </div>
                    </div>

                    <div class="circuit-region region-learning">
                        <div class="circuit-region-title">
                            <span class="circuit-region-dot"></span>
                            <span>学习资源</span>
                            <span class="circuit-region-count">${(circuit.learning || []).length} 项</span>
                        </div>
                        <div class="home-core-grid core-grid-2">${learningCards}</div>
                    </div>
                </div>
            </div>
        `;
        return;
    }
    
    // 通用分类页面
    breadcrumb += ` > <span class="breadcrumb-item">${cat.name}</span>`;
    
    let tags = getTagsByFocusCategory(categoryId);
    
    // 核心电路分类：显示五大电路卡片
    let circuitSection = '';
    if (categoryId === 'core_circuits') {
        circuitSection = `
            <div class="focus-circuits-bar">
                ${CORE_CIRCUITS.map(c => `
                    <button class="focus-circuit-pill ${circuitId === c.id ? 'active' : ''}" 
                            onclick="selectCoreCircuit('${c.id}')"
                            style="--pill-color: ${c.color};">
                        <span>${c.icon}</span>
                        <span>${c.name}</span>
                    </button>
                `).join('')}
            </div>
        `;
    }
    
    const tagCards = tags.map(tag => {
        const chapterInfo = getChapterInfoByTagId(tag.id);
        const types = (tag.types || []).map(t => {
            const qt = Object.values(QUESTION_TYPES).find(q => q.id === t);
            return qt ? `<span class="mini-tag" style="background: ${qt.color}20; color: ${qt.color};">${qt.name}</span>` : '';
        }).join('');
        const objectives = (tag.objectives || []).map(o => {
            const obj = Object.values(LEARNING_OBJECTIVES).find(q => q.id === o);
            return obj ? `<span class="mini-tag obj-tag">${obj.name}</span>` : '';
        }).join('');
        
        // 判断是否属于核心电路
        const circuit = CORE_CIRCUITS.find(c => c.tagIds.includes(tag.id));
        const circuitLabel = circuit ? `<span class="mini-tag circuit-tag" style="background: ${circuit.color}20; color: ${circuit.color};">${circuit.icon} ${circuit.name}</span>` : '';
        
        return `
            <div class="kp-card" style="--card-accent: ${circuit ? circuit.color : cat.color};" onclick="navigateToSection('${tag.id}')">
                <div class="kp-card-header">
                    <h4>${tag.name}</h4>
                </div>
                <div class="kp-card-meta">
                    ${chapterInfo && chapterInfo.chapter ? `<span class="kp-chapter">${chapterInfo.chapter}</span>` : ''}
                    ${chapterInfo && chapterInfo.topic ? `<span class="kp-chapter">知识体系</span>` : ''}
                </div>
                <div class="kp-card-tags">${circuitLabel}${types}${objectives}</div>
            </div>
        `;
    }).join('');
    
    contentArea.innerHTML = `
        <div class="content-header">
            <div class="breadcrumb" id="breadcrumb">${breadcrumb}</div>
            <div class="content-actions">
                <button class="btn" onclick="backToFocusHome()">← 返回</button>
            </div>
        </div>
        <div class="content-body" id="contentBody">
            <div class="focus-detail-view">
                <div class="focus-detail-hero" style="background: linear-gradient(135deg, ${cat.color}15, ${cat.color}05);">
                    <div class="focus-detail-icon" style="color: ${cat.color};">${cat.icon}</div>
                    <h2>${cat.name}</h2>
                    <p>${cat.description}</p>
                </div>
                <div class="focus-detail-stats">
                    <div class="focus-stat"><span class="stat-num">${tags.length}</span><span class="stat-label">知识点</span></div>
                </div>
                ${circuitSection}
                <h3 class="focus-section-title">相关知识点</h3>
                <div class="kp-grid">${tagCards}</div>
            </div>
        </div>
    `;
}

function backToFocusHome() {
    // 重点难点模块现挂在"交互式学习资源"页，返回到该页
    appState.focusCategory = null;
    appState.selectedCircuit = null;
    openLearningResources();
}

function navigateToSection(tagId) {
    // 切换到章节模式并选中对应小节
    const tag = KNOWLEDGE_TAGS.find(t => t.id === tagId);
    if (!tag) return;
    
    if (tag.category === 'chapter' && tag.type === 'section') {
        // 找到对应的课程章节
        for (const ch of courseData.chapters) {
            const sec = ch.sections.find(s => s.id === tagId);
            if (sec) {
                // 从学习资源进入，固定显示"学习资源"模块
                appState.currentModule = 'learning';
                document.querySelectorAll('.module-tab').forEach(tab => {
                    tab.classList.toggle('active', tab.dataset.module === 'learning');
                });
                switchView('chapter');
                appState.currentChapter = ch;
                appState.currentSection = sec;
                // 展开该章节
                appState.expandedChapters.add(ch.id);
                setTimeout(() => {
                    const chEl = document.querySelector(`.chapter-item[data-chapter-id="${ch.id}"]`);
                    if (chEl) chEl.classList.add('expanded');
                    renderSectionContent(sec);
                }, 100);
                return;
            }
        }
    }
    
    // 如果是知识体系标签，暂时提示
    // 后续可以跳转到知识图谱对应节点
    switchView('graph');
    setTimeout(() => {
        const node = document.querySelector(`.graph-node[data-id="${tagId}"]`);
        if (node) {
            node.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }
    }, 500);
}

function openResource(tagId, module) {
    switchModule(module);
    navigateToSection(tagId);
}

function renderSectionContent(section) {
    const contentBody = document.getElementById('contentBody');
    if (!contentBody) return;
    
    const chapter = appState.currentChapter;
    const moduleInfo = RESOURCE_MODULES[appState.currentModule.toUpperCase()];
    
    // 生成目标标签
    const objectiveTags = (section.objectives || []).map(objId => {
        const obj = Object.values(LEARNING_OBJECTIVES).find(o => o.id === objId);
        return obj ? `<span class="meta-tag objective">${obj.name}: ${obj.description}</span>` : '';
    }).join('');
    
    // 生成类型标签
    const typeTags = (section.types || []).map(typeId => {
        const type = Object.values(QUESTION_TYPES).find(t => t.id === typeId);
        return type ? `<span class="meta-tag type ${typeId}">${type.name}问题</span>` : '';
    }).join('');
    
    // 根据模块生成不同内容
    let moduleContent = '';
    
    switch (appState.currentModule) {
        case 'learning':
            moduleContent = renderLearningContent(section);
            break;
        case 'training':
            moduleContent = renderTrainingContent(section);
            break;
        case 'testing':
            moduleContent = renderTestingContent(section);
            break;
    }
    
    contentBody.innerHTML = `
        <div class="section-content-page">
            <div class="section-header">
                <div class="chapter-breadcrumb">${chapter.number} ${chapter.title}</div>
                <h2>${section.title}</h2>
                <div class="section-meta">
                    ${objectiveTags}
                    ${typeTags}
                    ${section.selfStudy ? '<span class="meta-tag" style="background: rgba(245, 158, 11, 0.1); color: #d97706;">自学内容</span>' : ''}
                    ${section.omitted ? '<span class="meta-tag" style="background: rgba(100, 116, 139, 0.1); color: #64748b;">省略内容</span>' : ''}
                </div>
            </div>
            ${moduleContent}
        </div>
    `;
}

function renderLearningContent(section) {
    const resources = [
        { icon: '📖', title: '电子教材', desc: '系统化的知识点讲解，配合图文详解', type: '教材' },
        { icon: '🎬', title: '视频讲解', desc: '名师授课视频，重难点深度解析', type: '视频' },
        { icon: '🎨', title: '动画演示', desc: '交互式动画，直观理解电路原理', type: '动画' },
        { icon: '📊', title: '课件PPT', desc: '课堂讲义课件，便于复习总结', type: '课件' },
        { icon: '🔌', title: '电路仿真', desc: '在线仿真实验，动手验证电路特性', type: '仿真' },
        { icon: '📋', title: '学习笔记', desc: '重点知识梳理，考试要点总结', type: '笔记' }
    ];
    
    return `
        <div class="resource-list">
            ${resources.map(r => `
                <div class="resource-card">
                    <div class="resource-card-header">
                        <div class="resource-icon">${r.icon}</div>
                        <div style="flex: 1;">
                            <h4>${r.title}</h4>
                            <p class="resource-desc">${r.desc}</p>
                        </div>
                    </div>
                    <div class="resource-card-footer">
                        <div class="resource-tags">
                            <span class="resource-tag">${r.type}</span>
                        </div>
                        <div class="resource-meta">
                            <span>点击进入 →</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderTrainingContent(section) {
    const exercises = [
        { icon: '💡', title: '典型例题解析', desc: '精选典型例题，详细解题步骤与思路分析', difficulty: 'easy', count: '5题' },
        { icon: '📝', title: '课后练习题', desc: '教材配套习题，巩固基础知识点', difficulty: 'medium', count: '10题' },
        { icon: '🎯', title: '提高训练题', desc: '进阶难度题目，提升分析解决问题能力', difficulty: 'hard', count: '8题' },
        { icon: '🔧', title: '设计性练习', desc: '开放式设计题，培养工程设计思维', difficulty: 'hard', count: '3题' },
        { icon: '🔌', title: '仿真实验', desc: '在线电路仿真，验证理论计算结果', difficulty: 'medium', count: '4个' },
        { icon: '📐', title: '考研真题', desc: '历年考研真题精选，深度解析', difficulty: 'hard', count: '6题' }
    ];
    
    const difficulties = {
        easy: { class: 'difficulty-easy', text: '基础' },
        medium: { class: 'difficulty-medium', text: '中等' },
        hard: { class: 'difficulty-hard', text: '困难' }
    };
    
    // 真实训练数据（data.js training 数组；带 lab 的条目可打开 16:9 交互电路界面）
    const items = (section && Array.isArray(section.training)) ? section.training : [];
    const dataCards = items.length ? `
        <div class="training-section">
            <h3 class="training-section-title">
                <span>🎮</span>
                <span>专项训练</span>
            </h3>
            <div class="training-grid">
                ${items.map(it => `
                    <div class="training-card ${it.lab ? 'has-lab' : ''}" ${it.lab ? `onclick="openCircuitLab('${it.lab}')"` : ''}>
                        <div class="training-card-header">
                            <div class="training-icon">${it.lab ? '🔬' : '📝'}</div>
                            <h4>${it.name}</h4>
                        </div>
                        <p>${it.desc || ''}${it.lab ? '<span class="lab-hint">点击进入交互电路</span>' : ''}</p>
                        <div class="training-card-footer">
                            <span class="difficulty-badge difficulty-medium">交互</span>
                            ${it.lab ? '<span class="question-count">进入 →</span>' : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    ` : '';

    return `
        ${dataCards}
        <div class="training-section">
            <h3 class="training-section-title">
                <span>📚</span>
                <span>练习题库</span>
            </h3>
            <div class="training-grid">
                ${exercises.map(e => `
                    <div class="training-card">
                        <div class="training-card-header">
                            <div class="training-icon">${e.icon}</div>
                            <h4>${e.title}</h4>
                        </div>
                        <p>${e.desc}</p>
                        <div class="training-card-footer">
                            <span class="difficulty-badge ${difficulties[e.difficulty].class}">
                                ${difficulties[e.difficulty].text}
                            </span>
                            <span class="question-count">${e.count}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function renderTestingContent(section) {
    const tests = [
        { type: '章节测验', title: '章节基础测验', desc: '覆盖本章核心知识点，检验基础掌握程度', questions: 15, time: '30分钟', score: '100分' },
        { type: '进阶测试', title: '能力提升测试', desc: '综合应用题型，考察分析解决问题能力', questions: 10, time: '45分钟', score: '100分' },
        { type: '设计考核', title: '电路设计考核', desc: '开放式设计题目，评估工程设计能力', questions: 3, time: '60分钟', score: '100分' }
    ];
    
    return `
        <div class="test-list">
            ${tests.map(t => `
                <div class="test-card">
                    <div class="test-card-header">
                        <h4>${t.title}</h4>
                        <span class="test-type-badge">${t.type}</span>
                    </div>
                    <div class="test-info">
                        <div class="test-info-item">
                            <span>📋</span>
                            <span>${t.questions} 道题</span>
                        </div>
                        <div class="test-info-item">
                            <span>⏱️</span>
                            <span>${t.time}</span>
                        </div>
                        <div class="test-info-item">
                            <span>💯</span>
                            <span>满分 ${t.score}</span>
                        </div>
                    </div>
                    <p class="test-desc">${t.desc}</p>
                    <div class="test-card-footer">
                        <span class="test-score">尚未参加考试</span>
                        <button class="btn btn-primary">开始测试 →</button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderExperimentContent(experiment) {
    const contentBody = document.getElementById('contentBody');
    if (!contentBody) return;
    
    const moduleInfo = RESOURCE_MODULES[appState.currentModule.toUpperCase()];
    
    contentBody.innerHTML = `
        <div class="section-content-page">
            <div class="section-header">
                <div class="chapter-breadcrumb">🧪 实验课程</div>
                <h2>${experiment.title}</h2>
                <div class="section-meta">
                    <span class="meta-tag objective">实验实践</span>
                    <span class="meta-tag type analysis">验证性实验</span>
                </div>
            </div>
            <div class="content-placeholder">
                <div class="content-placeholder-icon">🔬</div>
                <h3>实验内容建设中</h3>
                <p>该实验的${moduleInfo.name}正在建设中，敬请期待...</p>
            </div>
        </div>
    `;
}

function updateContentHeader() {
    const breadcrumb = document.getElementById('breadcrumb');
    if (!breadcrumb) return;
    
    let html = '<span class="breadcrumb-item" onclick="goHome()">首页</span>';
    
    if (appState.currentChapter && appState.currentSection) {
        html += `
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-item">${appState.currentChapter.title}</span>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-item current">${appState.currentSection.title}</span>
        `;
    }
    
    breadcrumb.innerHTML = html;
}

function goHome() {
    appState.currentSection = null;
    appState.currentChapter = null;
    document.querySelectorAll('.section-item, .subsection-item, .experiment-item').forEach(el => {
        el.classList.remove('active');
    });
    renderWelcomePage();
    updateContentHeader();
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}

// ==================== 知识图谱视图 ====================

// 图谱布局模式定义（可扩展）
const GRAPH_MODES = [
    { id: 'force', name: '模式1：力导向', icon: '◉', desc: '力导向布局' },
    { id: 'radial', name: '模式2：径向辐射', icon: '◎', desc: '径向辐射布局' }
];

// 当前图谱模式
appState.graphMode = 'force';
// 力导向动画帧ID
appState.graphAnimId = null;
// 节点位置缓存（力导向计算用）
appState.graphNodePositions = {};
appState.graphCategory = 'topic'; // 'topic' 知识体系 或 'chapter' 章节体系

// 层级颜色映射（保留兼容）
const LEVEL_COLORS = [
    '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#f97316',
    '#10b981', '#06b6d4', '#6366f1', '#ef4444', '#eab308', '#14b8a6'
];

const LEVEL_NAMES = [
    '基础概念', '半导体器件', '三极管', '基本放大电路', '多级放大',
    '模拟集成电路', '运放应用', '反馈电路', '功率放大', '信号处理', '直流电源'
];

// 图谱分类定义
const GRAPH_CATEGORIES = [
    { id: 'topic', name: '知识体系', icon: '🧠' },
    { id: 'chapter', name: '章节体系', icon: '📖' }
];

function initGraphView() {
}

function renderGraphView() {
    const contentArea = document.querySelector('.content-area');
    
    const modeButtons = GRAPH_MODES.map(m => 
        `<button class="graph-mode-btn ${m.id === appState.graphMode ? 'active' : ''}" data-mode="${m.id}" onclick="switchGraphMode('${m.id}')">
            <span class="mode-icon">${m.icon}</span>
            <span>${m.name}</span>
        </button>`
    ).join('');
    
    const categoryButtons = GRAPH_CATEGORIES.map(c =>
        `<button class="graph-cat-btn ${c.id === appState.graphCategory ? 'active' : ''}" data-cat="${c.id}" onclick="switchGraphCategory('${c.id}')">
            <span>${c.icon}</span>
            <span>${c.name}</span>
        </button>`
    ).join('');
    
    // 根据分类生成图例
    let legendItems = '';
    if (appState.graphCategory === 'topic') {
        // 知识体系图例：按一级分类
        Object.entries(TOPIC_CATEGORY_COLORS).forEach(([name, color]) => {
            legendItems += `<div class="legend-item">
                <span class="legend-dot" style="background: ${color};"></span>
                <span>${name}</span>
            </div>`;
        });
    } else {
        // 章节体系图例：按章节
        Object.entries(CHAPTER_COLORS).forEach(([id, color]) => {
            const chapter = courseData.chapters.find(ch => ch.id === id);
            const name = chapter ? `${chapter.number} ${chapter.title}` : (id === 'exp' ? '实验' : id);
            legendItems += `<div class="legend-item">
                <span class="legend-dot" style="background: ${color};"></span>
                <span>${name}</span>
            </div>`;
        });
    }
    
    contentArea.innerHTML = `
        <div class="content-header">
            <div class="breadcrumb" id="breadcrumb">
                <span class="breadcrumb-item">知识图谱</span>
            </div>
            <div class="content-actions">
                <button class="btn" onclick="switchView('chapter')">
                    <span>📚</span>
                    <span>返回章节</span>
                </button>
            </div>
        </div>
        <div class="graph-view" id="graphView">
            <div class="graph-mode-selector">
                <div class="graph-cat-switcher">${categoryButtons}</div>
                <div class="graph-mode-buttons">${modeButtons}</div>
            </div>
            <svg class="graph-canvas" id="graphCanvas"></svg>
            <div class="graph-legend">
                <div class="graph-legend-title">${appState.graphCategory === 'topic' ? '知识分类' : '章节分类'}</div>
                ${legendItems}
            </div>
            <div class="graph-controls">
                <button class="graph-control-btn" onclick="zoomGraph(1.2)" title="放大">+</button>
                <button class="graph-control-btn" onclick="zoomGraph(0.8)" title="缩小">−</button>
                <button class="graph-control-btn" onclick="resetGraph()" title="重置">⟲</button>
            </div>
            <div class="graph-tooltip" id="graphTooltip">
                <div class="graph-tooltip-title" id="tooltipTitle"></div>
                <div class="graph-tooltip-chapter" id="tooltipChapter"></div>
                <div class="graph-tooltip-info" id="tooltipInfo"></div>
            </div>
        </div>
    `;
    
    drawGraphByMode(appState.graphMode);
    initGraphInteractions();
}

// 切换图谱分类（知识体系/章节体系）
function switchGraphCategory(cat) {
    if (appState.graphCategory === cat) return;
    appState.graphCategory = cat;
    
    // 更新按钮状态
    document.querySelectorAll('.graph-cat-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.cat === cat);
    });
    
    // 重新绘制
    drawGraphByMode(appState.graphMode);
    
    // 重新生成图例
    const legendTitle = document.querySelector('.graph-legend-title');
    const legendBox = document.querySelector('.graph-legend');
    if (legendTitle) legendTitle.textContent = cat === 'topic' ? '知识分类' : '章节分类';
    
    // 重新生成图例项
    let legendItems = '';
    if (cat === 'topic') {
        Object.entries(TOPIC_CATEGORY_COLORS).forEach(([name, color]) => {
            legendItems += `<div class="legend-item">
                <span class="legend-dot" style="background: ${color};"></span>
                <span>${name}</span>
            </div>`;
        });
    } else {
        Object.entries(CHAPTER_COLORS).forEach(([id, color]) => {
            const chapter = courseData.chapters.find(ch => ch.id === id);
            const name = chapter ? `${chapter.number} ${chapter.title}` : (id === 'exp' ? '实验' : id);
            legendItems += `<div class="legend-item">
                <span class="legend-dot" style="background: ${color};"></span>
                <span>${name}</span>
            </div>`;
        });
    }
    if (legendBox) {
        const title = legendBox.querySelector('.graph-legend-title');
        legendBox.innerHTML = '';
        legendBox.appendChild(title);
        legendBox.insertAdjacentHTML('beforeend', legendItems);
    }
    
    // 重置视图
    if (appState.graphMode === 'radial') {
        resetGraph();
    } else {
        appState.graph.scale = 1;
        appState.graph.translateX = 0;
        appState.graph.translateY = 0;
        updateGraphTransform();
    }
}

function switchGraphMode(mode) {
    // 停止之前的动画
    if (appState.graphAnimId) {
        cancelAnimationFrame(appState.graphAnimId);
        appState.graphAnimId = null;
    }
    
    appState.graphMode = mode;
    
    // 更新按钮状态
    document.querySelectorAll('.graph-mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    drawGraphByMode(mode);
    
    // 根据模式调整初始视图
    if (mode === 'radial') {
        resetGraph(); // 自动缩放到全图可见
    } else {
        appState.graph.scale = 1;
        appState.graph.translateX = 0;
        appState.graph.translateY = 0;
        updateGraphTransform();
    }
}

function drawGraphByMode(mode) {
    const svg = document.getElementById('graphCanvas');
    if (!svg) return;
    
    // 清空SVG
    svg.innerHTML = '';
    
    // 获取容器尺寸
    const view = document.getElementById('graphView');
    const viewW = view ? view.clientWidth : 1200;
    const viewH = view ? view.clientHeight : 800;
    
    const canvasW = viewW;
    const canvasH = viewH;
    
    svg.setAttribute('width', canvasW);
    svg.setAttribute('height', canvasH);
    svg.setAttribute('viewBox', `0 0 ${canvasW} ${canvasH}`);
    svg.style.width = canvasW + 'px';
    svg.style.height = canvasH + 'px';
    
    // 根据当前分类从标签体系生成图谱数据
    const data = generateGraphFromTags(appState.graphCategory);
    
    // 计算节点位置
    let positions;
    if (mode === 'force') {
        positions = computeForceLayout(data, canvasW, canvasH);
    } else {
        positions = computeRadialLayout(data, canvasW, canvasH);
    }
    
    // 绘制环（仅径向模式）
    if (mode === 'radial') {
        drawRadialRings(svg, positions, canvasW, canvasH);
    }
    
    // 绘制连线
    const linksGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    linksGroup.setAttribute('id', 'graphLinks');
    
    // 计算中心节点（用于径向模式判断）
    let hubId = null;
    let hubDegree = 0;
    const degreeMap = new Map();
    data.links.forEach(link => {
        degreeMap.set(link.source, (degreeMap.get(link.source) || 0) + 1);
        degreeMap.set(link.target, (degreeMap.get(link.target) || 0) + 1);
    });
    degreeMap.forEach((deg, id) => {
        if (deg > hubDegree) { hubDegree = deg; hubId = id; }
    });
    
    data.links.forEach(link => {
        const source = positions.get(link.source);
        const target = positions.get(link.target);
        if (!source || !target) return;
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('class', 'graph-link');
        path.setAttribute('data-source', link.source);
        path.setAttribute('data-target', link.target);
        
        const sourceNode = data.nodes.find(n => n.id === link.source);
        const targetNode = data.nodes.find(n => n.id === link.target);
        const sourceColor = sourceNode.color || '#64748b';
        
        const dx = target.x - source.x;
        const dy = target.y - source.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (mode === 'force') {
            // 力导向模式：贝塞尔曲线，更有机的连线
            const mx = (source.x + target.x) / 2;
            const my = (source.y + target.y) / 2;
            const offsetX = dy * 0.2;
            const offsetY = -dx * 0.2;
            const d = `M ${source.x} ${source.y} Q ${mx + offsetX} ${my + offsetY} ${target.x} ${target.y}`;
            path.setAttribute('d', d);
            path.setAttribute('stroke', sourceColor);
            path.setAttribute('stroke-width', '1.5');
            path.setAttribute('opacity', '0.25');
        } else {
            // 径向模式：直线连接，更规整
            // 与中心节点相连的线更粗更亮
            const isHubLink = (link.source === hubId || link.target === hubId);
            const d = `M ${source.x} ${source.y} L ${target.x} ${target.y}`;
            path.setAttribute('d', d);
            path.setAttribute('stroke', sourceColor);
            path.setAttribute('stroke-width', isHubLink ? '2' : '1.2');
            path.setAttribute('opacity', isHubLink ? '0.55' : '0.2');
        }
        
        linksGroup.appendChild(path);
    });
    svg.appendChild(linksGroup);
    
    // 绘制节点
    const nodesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodesGroup.setAttribute('id', 'graphNodes');
    
    const centerX = canvasW / 2;
    const centerY = canvasH / 2;
    const maxRadius = Math.min(canvasW, canvasH) * 0.42;
    
    data.nodes.forEach(node => {
        const pos = positions.get(node.id);
        if (!pos) return;
        
        const degree = degreeMap.get(node.id) || 0;
        const color = node.color || '#64748b';
        const isHub = node.id === hubId;
        
        // 根据模式计算节点大小
        let radius;
        if (mode === 'force') {
            // 力导向模式：节点大小按连接数微调，差距不大
            radius = 16 + degree * 2;
        } else {
            // 径向模式：中心节点大，向外逐渐缩小，突出圆环感
            const dx = pos.x - centerX;
            const dy = pos.y - centerY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const distRatio = Math.min(1, dist / maxRadius);
            if (isHub) {
                radius = 28; // 中心枢纽节点
            } else {
                radius = 18 - distRatio * 6; // 越往外越小
                radius = Math.max(10, radius);
            }
        }
        
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'graph-node' + (isHub ? ' is-hub' : ''));
        g.setAttribute('data-node-id', node.id);
        g.setAttribute('data-level', node.level);
        g.setAttribute('transform', `translate(${pos.x}, ${pos.y})`);
        
        // 节点光晕（中心节点/高连接数节点）
        if (isHub) {
            const glowSize = mode === 'radial' ? radius + 18 : radius + 8;
            const glowOpacity = mode === 'radial' ? '0.25' : '0.12';
            const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            glow.setAttribute('r', glowSize);
            glow.setAttribute('fill', color);
            glow.setAttribute('opacity', glowOpacity);
            g.appendChild(glow);
            
            // 径向模式下再加一层外光晕
            if (mode === 'radial') {
                const glow2 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                glow2.setAttribute('r', radius + 30);
                glow2.setAttribute('fill', color);
                glow2.setAttribute('opacity', '0.1');
                g.appendChild(glow2);
            }
        }
        
        // 节点圆
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('r', radius);
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', isHub ? '#fff' : 'rgba(255,255,255,0.3)');
        circle.setAttribute('stroke-width', isHub ? '2.5' : '1.5');
        g.appendChild(circle);
        
        // 节点文字
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.textContent = node.name;
        if (radius < 24) {
            // 小节点文字放在下方
            text.setAttribute('class', 'label-below');
            text.setAttribute('y', radius + 6);
            text.setAttribute('fill', 'rgba(255,255,255,0.7)');
            text.style.fontSize = '10px';
        } else {
            text.setAttribute('fill', 'white');
        }
        g.appendChild(text);
        
        // 交互
        g.addEventListener('mouseenter', (e) => showGraphTooltip(e, node, degree));
        g.addEventListener('mouseleave', hideGraphTooltip);
        g.addEventListener('click', () => onGraphNodeClick(node));
        
        // 力导向模式下支持拖拽节点
        if (appState.graphMode === 'force') {
            let isDraggingNode = false;
            g.addEventListener('mousedown', (e) => {
                e.stopPropagation();
                isDraggingNode = true;
                g.style.cursor = 'grabbing';
            });
            g.addEventListener('mousemove', (e) => {
                if (!isDraggingNode) return;
                const pt = svg.createSVGPoint();
                pt.x = e.clientX;
                pt.y = e.clientY;
                const svgPt = pt.matrixTransform(svg.getScreenCTM().inverse());
                const newTransform = `translate(${svgPt.x}, ${svgPt.y})`;
                g.setAttribute('transform', newTransform);
                pos.x = svgPt.x;
                pos.y = svgPt.y;
                updateNodeLinks(svg, node.id, pos);
            });
            g.addEventListener('mouseup', () => {
                isDraggingNode = false;
                g.style.cursor = 'pointer';
            });
            g.addEventListener('mouseleave', () => {
                isDraggingNode = false;
                g.style.cursor = 'pointer';
            });
        }
        
        nodesGroup.appendChild(g);
    });
    svg.appendChild(nodesGroup);
}

// 力导向布局算法
function computeForceLayout(data, canvasW, canvasH) {
    const positions = new Map();
    const centerX = canvasW / 2;
    const centerY = canvasH / 2;
    
    // 初始化：大范围随机散布，更有有机感
    data.nodes.forEach((node, i) => {
        positions.set(node.id, {
            x: centerX + (Math.random() - 0.5) * canvasW * 0.6,
            y: centerY + (Math.random() - 0.5) * canvasH * 0.6,
            vx: 0,
            vy: 0
        });
    });
    
    const iterationCount = 500;
    const k = 95;          // 理想边长度
    const repulsion = 12000; // 更强的排斥力，让节点更散开
    const attraction = 0.025; // 较弱的吸引力
    const damping = 0.82;
    const centerForce = 0.005; // 很弱的中心引力，让布局更自由
    
    const nodeArr = data.nodes;
    
    for (let iter = 0; iter < iterationCount; iter++) {
        const t = 1 - iter / iterationCount; // 温度衰减
        
        // 排斥力（所有节点对）
        for (let i = 0; i < nodeArr.length; i++) {
            const posA = positions.get(nodeArr[i].id);
            for (let j = i + 1; j < nodeArr.length; j++) {
                const posB = positions.get(nodeArr[j].id);
                const dx = posA.x - posB.x;
                const dy = posA.y - posB.y;
                const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                const force = repulsion / (dist * dist);
                const fx = (dx / dist) * force;
                const fy = (dy / dist) * force;
                posA.vx += fx * t;
                posA.vy += fy * t;
                posB.vx -= fx * t;
                posB.vy -= fy * t;
            }
        }
        
        // 吸引力（连接的节点）
        data.links.forEach(link => {
            const posA = positions.get(link.source);
            const posB = positions.get(link.target);
            if (!posA || !posB) return;
            const dx = posB.x - posA.x;
            const dy = posB.y - posA.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const force = attraction * (dist - k);
            const fx = (dx / dist) * force * 100;
            const fy = (dy / dist) * force * 100;
            posA.vx += fx * t;
            posA.vy += fy * t;
            posB.vx -= fx * t;
            posB.vy -= fy * t;
        });
        
        // 很弱的中心引力 + 更新位置
        positions.forEach((pos) => {
            pos.vx += (centerX - pos.x) * centerForce * t;
            pos.vy += (centerY - pos.y) * centerForce * t;
            pos.vx *= damping;
            pos.vy *= damping;
            pos.x += pos.vx * t;
            pos.y += pos.vy * t;
            
            // 边界约束（宽松一点，让布局更自然）
            const margin = 40;
            pos.x = Math.max(margin, Math.min(canvasW - margin, pos.x));
            pos.y = Math.max(margin, Math.min(canvasH - margin, pos.y));
        });
    }
    
    // 清理速度属性
    positions.forEach(pos => {
        delete pos.vx;
        delete pos.vy;
    });
    
    return positions;
}

// 径向辐射布局算法（按BFS最短路径分圈）
function computeRadialLayout(data, canvasW, canvasH) {
    const positions = new Map();
    const centerX = canvasW / 2;
    const centerY = canvasH / 2;
    
    // 圆环半径：画布短边的85%，配合缩放可看清细节
    const maxRadius = Math.min(canvasW, canvasH) * 0.85;
    
    // 构建邻接表
    const adj = new Map();
    data.nodes.forEach(node => adj.set(node.id, []));
    data.links.forEach(link => {
        if (adj.has(link.source) && adj.has(link.target)) {
            adj.get(link.source).push(link.target);
            adj.get(link.target).push(link.source);
        }
    });
    
    // 计算每个节点的度，找中心节点
    const degreeMap = new Map();
    data.links.forEach(link => {
        degreeMap.set(link.source, (degreeMap.get(link.source) || 0) + 1);
        degreeMap.set(link.target, (degreeMap.get(link.target) || 0) + 1);
    });
    
    let hubId = data.nodes[0].id;
    let maxDegree = 0;
    degreeMap.forEach((deg, id) => {
        if (deg > maxDegree) {
            maxDegree = deg;
            hubId = id;
        }
    });
    
    // BFS计算每个节点到中心的距离（第几圈）
    const distance = new Map();
    const queue = [hubId];
    distance.set(hubId, 0);
    
    while (queue.length > 0) {
        const current = queue.shift();
        const neighbors = adj.get(current) || [];
        neighbors.forEach(next => {
            if (!distance.has(next)) {
                distance.set(next, distance.get(current) + 1);
                queue.push(next);
            }
        });
    }
    
    // 未连通的节点，放在最外圈
    data.nodes.forEach(node => {
        if (!distance.has(node.id)) {
            distance.set(node.id, 99); // 标记为最外圈
        }
    });
    
    // 按距离分组（同一圈的节点）
    const ringGroups = {};
    distance.forEach((dist, id) => {
        const key = dist === 99 ? 'outer' : dist;
        if (!ringGroups[key]) ringGroups[key] = [];
        ringGroups[key].push(id);
    });
    
    // 计算有多少个有效环（不含中心）
    const ringKeys = Object.keys(ringGroups)
        .filter(k => k !== '0' && k !== 'outer')
        .map(Number)
        .sort((a, b) => a - b);
    
    const numRings = ringKeys.length + (ringGroups.outer ? 1 : 0);
    const ringSpacing = numRings > 0 ? maxRadius / (numRings + 1) : maxRadius / 3;
    
    // 中心节点
    positions.set(hubId, { x: centerX, y: centerY });
    
    // 每一圈均匀分布节点
    ringKeys.forEach((ringIdx, i) => {
        const nodeIds = ringGroups[ringIdx];
        const radius = ringSpacing * (i + 1);
        
        // 均匀分布在圆环上，从顶部开始
        nodeIds.forEach((nodeId, j) => {
            const angle = (j / nodeIds.length) * Math.PI * 2 - Math.PI / 2;
            positions.set(nodeId, {
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius
            });
        });
    });
    
    // 最外圈（未连通的节点）
    if (ringGroups.outer) {
        const outerRadius = maxRadius;
        ringGroups.outer.forEach((nodeId, j) => {
            const angle = (j / ringGroups.outer.length) * Math.PI * 2 - Math.PI / 2;
            positions.set(nodeId, {
                x: centerX + Math.cos(angle) * outerRadius,
                y: centerY + Math.sin(angle) * outerRadius
            });
        });
    }
    
    return positions;
}

// 绘制径向模式的环
function drawRadialRings(svg, positions, canvasW, canvasH) {
    const centerX = canvasW / 2;
    const centerY = canvasH / 2;
    
    const ringsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    ringsGroup.setAttribute('id', 'graphRings');
    
    // 找到所有节点中不同的半径值（即不同的环）
    const ringRadii = new Set();
    positions.forEach(pos => {
        const dx = pos.x - centerX;
        const dy = pos.y - centerY;
        const r = Math.sqrt(dx * dx + dy * dy);
        if (r > 5) ringRadii.add(Math.round(r));
    });
    
    // 按半径排序，绘制每个环
    const sortedRadii = Array.from(ringRadii).sort((a, b) => a - b);
    sortedRadii.forEach((r, idx) => {
        const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        ring.setAttribute('class', 'graph-ring');
        ring.setAttribute('cx', centerX);
        ring.setAttribute('cy', centerY);
        ring.setAttribute('r', r);
        
        // 最内圈和最外圈用实线，更突出
        const isOutermost = idx === sortedRadii.length - 1;
        if (isOutermost) {
            ring.setAttribute('stroke', 'rgba(99, 102, 241, 0.4)');
            ring.setAttribute('stroke-width', '2');
            ring.setAttribute('stroke-dasharray', 'none');
        } else if (idx === 0) {
            ring.setAttribute('stroke', 'rgba(255, 255, 255, 0.2)');
            ring.setAttribute('stroke-width', '1.5');
            ring.setAttribute('stroke-dasharray', 'none');
        }
        
        ringsGroup.appendChild(ring);
    });
    
    svg.appendChild(ringsGroup);
}

// 更新拖拽节点的连线
function updateNodeLinks(svg, nodeId, pos) {
    const links = svg.querySelectorAll('.graph-link');
    links.forEach(link => {
        const sourceId = link.dataset.source;
        const targetId = link.dataset.target;
        if (sourceId !== nodeId && targetId !== nodeId) return;
        
        const data = generateGraphFromTags(appState.graphCategory);
        const sourceNode = data.nodes.find(n => n.id === sourceId);
        const targetNode = data.nodes.find(n => n.id === targetId);
        
        // 获取节点位置
        const sourceG = svg.querySelector(`.graph-node[data-node-id="${sourceId}"]`);
        const targetG = svg.querySelector(`.graph-node[data-node-id="${targetId}"]`);
        if (!sourceG || !targetG) return;
        
        const sourceTransform = sourceG.getAttribute('transform').match(/translate\(([^,]+),\s*([^)]+)\)/);
        const targetTransform = targetG.getAttribute('transform').match(/translate\(([^,]+),\s*([^)]+)\)/);
        if (!sourceTransform || !targetTransform) return;
        
        const sx = parseFloat(sourceTransform[1]);
        const sy = parseFloat(sourceTransform[2]);
        const tx = parseFloat(targetTransform[1]);
        const ty = parseFloat(targetTransform[2]);
        
        const mx = (sx + tx) / 2;
        const my = (sy + ty) / 2;
        const dx = tx - sx;
        const dy = ty - sy;
        const offsetX = dy * 0.15;
        const offsetY = -dx * 0.15;
        
        const d = `M ${sx} ${sy} Q ${mx + offsetX} ${my + offsetY} ${tx} ${ty}`;
        link.setAttribute('d', d);
    });
}

function initGraphInteractions() {
    const view = document.getElementById('graphView');
    const canvas = document.getElementById('graphCanvas');
    if (!view || !canvas) return;
    
    // 拖拽平移
    view.addEventListener('mousedown', (e) => {
        if (e.target.closest('.graph-node') || e.target.closest('.graph-mode-btn') || 
            e.target.closest('.graph-control-btn') || e.target.closest('.graph-legend')) return;
        appState.graph.isDragging = true;
        appState.graph.startX = e.clientX - appState.graph.translateX;
        appState.graph.startY = e.clientY - appState.graph.translateY;
        view.style.cursor = 'grabbing';
    });
    
    let mouseMoveHandler = (e) => {
        if (!appState.graph.isDragging) return;
        appState.graph.translateX = e.clientX - appState.graph.startX;
        appState.graph.translateY = e.clientY - appState.graph.startY;
        updateGraphTransform();
    };
    
    let mouseUpHandler = () => {
        appState.graph.isDragging = false;
        const v = document.getElementById('graphView');
        if (v) v.style.cursor = 'grab';
    };
    
    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
    
    // 滚轮缩放
    view.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        const newScale = appState.graph.scale * delta;
        if (newScale >= 0.1 && newScale <= 8) {
            appState.graph.scale = newScale;
            updateGraphTransform();
        }
    }, { passive: false });
}

function updateGraphTransform() {
    const canvas = document.getElementById('graphCanvas');
    if (!canvas) return;
    canvas.style.transform = `translate(${appState.graph.translateX}px, ${appState.graph.translateY}px) scale(${appState.graph.scale})`;
    canvas.style.transformOrigin = '0 0';
}

function zoomGraph(factor) {
    const newScale = appState.graph.scale * factor;
    if (newScale >= 0.1 && newScale <= 8) {
        appState.graph.scale = newScale;
        updateGraphTransform();
    }
}

function resetGraph() {
    // 径向模式下自动缩放到能看到全图
    if (appState.graphMode === 'radial') {
        const canvas = document.getElementById('graphCanvas');
        const container = document.getElementById('graphView');
        if (canvas && container) {
            const canvasW = canvas.getAttribute('width');
            const canvasH = canvas.getAttribute('height');
            const containerW = container.clientWidth - 320; // 减去图例宽度
            const containerH = container.clientHeight - 120;
            
            // 计算需要的缩放比例（图谱直径约为短边*1.7）
            const graphSize = Math.min(canvasW, canvasH) * 1.7;
            const scale = Math.min(containerW, containerH) / graphSize;
            appState.graph.scale = Math.max(0.1, Math.min(1, scale));
            
            // 居中
            appState.graph.translateX = (containerW - canvasW * appState.graph.scale) / 2 + 160;
            appState.graph.translateY = (containerH - canvasH * appState.graph.scale) / 2 + 60;
        }
    } else {
        appState.graph.scale = 1;
        appState.graph.translateX = 0;
        appState.graph.translateY = 0;
    }
    updateGraphTransform();
}

function showGraphTooltip(e, node, degree) {
    const tooltip = document.getElementById('graphTooltip');
    const view = document.getElementById('graphView');
    if (!tooltip || !view) return;
    
    // 找到父级标签名称
    const tagInfo = KNOWLEDGE_TAGS.find(t => t.id === node.id);
    let parentName = '';
    if (tagInfo && tagInfo.parent) {
        const parentTag = KNOWLEDGE_TAGS.find(t => t.id === tagInfo.parent);
        if (parentTag) parentName = parentTag.name;
    }
    
    const typeName = node.category === 'topic' ? '知识体系' : '章节体系';
    const typeLabel = node.tagType ? {root: '根节点', topic: '知识分类', chapter: '章节', section: '知识点', knowledge: '知识点'}[node.tagType] || node.tagType : '';
    
    document.getElementById('tooltipTitle').textContent = node.name;
    document.getElementById('tooltipChapter').textContent = parentName ? `所属: ${parentName}` : typeName;
    document.getElementById('tooltipInfo').textContent = `${typeLabel} · 层级: ${node.level} · 子节点: ${node.childCount || 0}`;
    
    const rect = view.getBoundingClientRect();
    let tx = e.clientX - rect.left + 15;
    let ty = e.clientY - rect.top + 15;
    
    // 防止超出右边界
    if (tx > rect.width - 220) tx = e.clientX - rect.left - 215;
    if (ty > rect.height - 80) ty = e.clientY - rect.top - 65;
    
    tooltip.style.left = tx + 'px';
    tooltip.style.top = ty + 'px';
    tooltip.style.display = 'block';
    
    // 高亮相关连线和节点
    const connectedIds = new Set([node.id]);
    document.querySelectorAll('.graph-link').forEach(link => {
        const isRelated = link.dataset.source === node.id || link.dataset.target === node.id;
        if (isRelated) {
            link.classList.add('highlighted');
            link.classList.remove('dimmed');
            connectedIds.add(link.dataset.source);
            connectedIds.add(link.dataset.target);
        } else {
            link.classList.add('dimmed');
        }
    });
    
    document.querySelectorAll('.graph-node').forEach(n => {
        if (!connectedIds.has(n.dataset.nodeId)) {
            n.classList.add('dimmed');
        } else {
            n.classList.remove('dimmed');
        }
    });
}

function hideGraphTooltip() {
    const tooltip = document.getElementById('graphTooltip');
    if (tooltip) tooltip.style.display = 'none';
    
    document.querySelectorAll('.graph-link').forEach(link => {
        link.classList.remove('highlighted');
        link.classList.remove('dimmed');
    });
    document.querySelectorAll('.graph-node').forEach(n => {
        n.classList.remove('dimmed');
    });
}

function onGraphNodeClick(node) {
    const chapter = courseData.chapters.find(ch => ch.id === node.chapter);
    if (chapter) {
        const chapterEl = document.querySelector(`.chapter-item[data-chapter-id="${chapter.id}"]`);
        if (chapterEl && !chapterEl.classList.contains('expanded')) {
            toggleChapter(chapter.id);
        }
        
        let matchedSection = null;
        chapter.sections.forEach(section => {
            const cleanTitle = section.title.replace(/（.*）/, '').replace(/\(.*\)/, '');
            if (section.title.includes(node.name) || node.name.includes(cleanTitle)) {
                matchedSection = section;
            }
            if (section.subsections) {
                section.subsections.forEach(sub => {
                    const subClean = sub.title.replace(/（.*）/, '').replace(/\(.*\)/, '');
                    if (sub.title.includes(node.name) || node.name.includes(subClean)) {
                        matchedSection = sub;
                    }
                });
            }
        });
        
        switchView('chapter');
        
        if (matchedSection) {
            selectSection(matchedSection, chapter);
        } else {
            appState.currentChapter = chapter;
            goHome();
        }
    }
}
