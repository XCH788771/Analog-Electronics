/**
 * 模拟电子技术课程数据
 * 包含章节结构、知识点、问题类型分类等
 */

// 问题类型
const QUESTION_TYPES = {
    CALCULATION: { id: 'calculation', name: '计算类', color: '#e74c3c' },
    ANALYSIS: { id: 'analysis', name: '分析类', color: '#3498db' },
    DESIGN: { id: 'design', name: '设计类', color: '#2ecc71' }
};

// 教学目标
const LEARNING_OBJECTIVES = {
    GOAL1: { id: 'goal1', name: '目标1', description: '知识理解与记忆', color: '#9b59b6' },
    GOAL2: { id: 'goal2', name: '目标2', description: '分析与应用能力', color: '#f39c12' },
    GOAL3: { id: 'goal3', name: '目标3', description: '综合设计与创新', color: '#1abc9c' }
};

// 资源模块类型
const RESOURCE_MODULES = {
    LEARNING: { id: 'learning', name: '学习资源', icon: '📚' },
    TRAINING: { id: 'training', name: '训练资源', icon: '✏️' },
    TESTING: { id: 'testing', name: '测试资源', icon: '📝' }
};

// 课程章节数据
const courseData = {
    title: '模拟电子技术',
    subtitle: 'Analog Electronic Technology',
    chapters: [
        {
            id: 'ch1',
            number: '第一章',
            title: '绪论',
            sections: [
                { id: 'ch1-1', title: '信号', objectives: ['goal1'], types: ['analysis'] },
                { id: 'ch1-2', title: '信号的频谱', objectives: ['goal1', 'goal2'], types: ['calculation', 'analysis'] },
                { id: 'ch1-3', title: '模拟信号和数字信号', objectives: ['goal1'], types: ['analysis'] },
                { id: 'ch1-4', title: '放大电路模型', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch1-5', title: '放大电路的主要性能指标', objectives: ['goal1', 'goal2'], types: ['calculation', 'analysis'] }
            ]
        },
        {
            id: 'ch2',
            number: '第二章',
            title: '运算放大器',
            sections: [
                { id: 'ch2-1', title: '集成电路运算放大器', objectives: ['goal1'], types: ['analysis'] },
                { id: 'ch2-2', title: '理想运算放大器', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch2-3', title: '基本线性运放电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch2-4', title: '同相输入和反相输入放大电路的其它应用', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] }
            ]
        },
        {
            id: 'ch3',
            number: '第三章',
            title: '二极管及基本电路',
            sections: [
                { id: 'ch3-1', title: '半导体的基本知识', objectives: ['goal1'], types: ['analysis'] },
                { id: 'ch3-2', title: 'PN 结的形成及特性', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch3-3', title: '二极管', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch3-4', title: '二极管的基本电路及其分析方法', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch3-5', title: '特殊二极管', objectives: ['goal1', 'goal2'], types: ['analysis'] }
            ]
        },
        {
            id: 'ch4',
            number: '第四章',
            title: '场效应三极管及其放大电路',
            sections: [
                { id: 'ch4-1', title: '金属-氧化物-半导体（MOS）场效应三极管', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch4-2', title: 'MOSFET 基本共源放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch4-4', title: '小信号模型分析法', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
                { id: 'ch4-5', title: '共漏极和共栅极放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch4-6', title: 'MOSFET 大信号工作及开关应用（省略）', objectives: ['goal1'], types: ['analysis'], omitted: true },
                { id: 'ch4-7', title: '多级放大电路（省略）', objectives: ['goal2'], types: ['analysis'], omitted: true },
                { id: 'ch4-8', title: '结型场效应管（JFET）及其放大电路（省略）', objectives: ['goal1'], types: ['analysis'], omitted: true }
            ]
        },
        {
            id: 'ch5',
            number: '第五章',
            title: '双极结型三极管（BJT）及其放大电路',
            sections: [
                { id: 'ch5-1', title: 'BJT', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                {
                    id: 'ch5-2',
                    title: 'BJT 放大电路',
                    subsections: [
                        { id: 'ch5-2-1', title: '基本共射极放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                        { id: 'ch5-2-2', title: 'BJT 放大电路的图解分析', objectives: ['goal2'], types: ['analysis'] },
                        { id: 'ch5-2-3', title: 'BJT 的小信号模型', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
                        { id: 'ch5-2-4', title: '共射极放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                        { id: 'ch5-2-5', title: '共集电极和共基极放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] }
                    ]
                },
                { id: 'ch5-3', title: 'FET 和 BJT 及其基本放大电路性能的比较（自学）', objectives: ['goal2'], types: ['analysis'], selfStudy: true },
                { id: 'ch5-4', title: '多级放大电路（简略）', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'], brief: true }
            ]
        },
        {
            id: 'ch7',
            number: '第七章',
            title: '模拟集成电路',
            sections: [
                { id: 'ch7-1', title: '模拟集成电路中的直流偏置技术（FET 的自学）', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'], selfStudy: true },
                { id: 'ch7-2', title: '差分式放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch7-4', title: '集成运算放大器电路简介', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch7-5', title: '实际运算放大器的主要参数和相关应用问题', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
                { id: 'ch7-6', title: '变跨导式模拟乘法器（省略）', objectives: ['goal1'], types: ['analysis'], omitted: true },
                { id: 'ch7-7', title: '放大电路中的噪声与干扰（自学）', objectives: ['goal2'], types: ['analysis'], selfStudy: true }
            ]
        },
        {
            id: 'ch8',
            number: '第八章',
            title: '反馈放大电路',
            sections: [
                { id: 'ch8-1', title: '反馈的基本概念与分类', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch8-2', title: '负反馈放大电路增益的一般表达式', objectives: ['goal2'], types: ['calculation', 'analysis'] },
                { id: 'ch8-3', title: '负反馈对放大电路性能的影响', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
                { id: 'ch8-4', title: '深度负反馈条件下的近似计算', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
                { id: 'ch8-5', title: '负反馈放大电路设计（自学）', objectives: ['goal3'], types: ['design'], selfStudy: true },
                { id: 'ch8-6', title: '负反馈放大电路的稳定性（自学）', objectives: ['goal2', 'goal3'], types: ['analysis'], selfStudy: true }
            ]
        },
        {
            id: 'ch9',
            number: '第九章',
            title: '功率放大电路',
            sections: [
                { id: 'ch9-1', title: '功率放大电路的一般问题', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch9-2', title: '射极输出器 —— 甲类放大的实例（自学）', objectives: ['goal2'], types: ['calculation', 'analysis'], selfStudy: true },
                { id: 'ch9-3', title: '乙类双电源互补对称功率放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch9-4', title: '甲乙类互补对称功率放大电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch9-5', title: '丁类 (D 类) 功率放大电路原理（省略）', objectives: ['goal1'], types: ['analysis'], omitted: true },
                { id: 'ch9-6', title: '功率管', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch9-7', title: '集成功率放大器举例', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] }
            ]
        },
        {
            id: 'ch10',
            number: '第十章',
            title: '信号处理与信号产生电路',
            sections: [
                { id: 'ch10-1', title: '滤波电路的基本概念与分类', objectives: ['goal1', 'goal2'], types: ['analysis'] },
                { id: 'ch10-2', title: '一阶有源滤波电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch10-3', title: '高阶有源滤波电路（自学）', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'], selfStudy: true },
                { id: 'ch10-5', title: '正弦波振荡电路的振荡条件', objectives: ['goal2'], types: ['analysis'] },
                { id: 'ch10-6', title: 'RC 正弦波振荡电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch10-7', title: 'LC 正弦波振荡电路（省略，高频课程讲）', objectives: ['goal1'], types: ['analysis'], omitted: true },
                { id: 'ch10-8', title: '非正弦信号产生电路（自学）', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'], selfStudy: true }
            ]
        },
        {
            id: 'ch11',
            number: '第十一章',
            title: '直流稳压电源',
            sections: [
                { id: 'ch11-1', title: '小功率整流滤波电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch11-2', title: '线性稳压电路', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
                { id: 'ch11-3', title: '开关式稳压电路（省略）', objectives: ['goal1'], types: ['analysis'], omitted: true }
            ]
        }
    ],
    experiments: [
        { id: 'exp1', title: '实验一 晶体管放大电路指标测试', chapter: 'ch5', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
        { id: 'exp2', title: '实验二 集成运放应用电路及指标测试', chapter: 'ch2', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
        { id: 'exp3', title: '实验三 功率放大器指标测试', chapter: 'ch9', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
        { id: 'exp4', title: '实验四 信号发生器指标参数测试', chapter: 'ch10', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] }
    ]
};

// 知识图谱节点数据（用于知识图谱视图）
const knowledgeGraphData = {
    nodes: [
        // 基础概念层
        { id: 'signal', name: '信号', chapter: 'ch1', level: 0, x: 400, y: 50 },
        { id: 'spectrum', name: '信号频谱', chapter: 'ch1', level: 0, x: 600, y: 50 },
        
        // 半导体器件层
        { id: 'semiconductor', name: '半导体基础', chapter: 'ch3', level: 1, x: 200, y: 150 },
        { id: 'pn_junction', name: 'PN结', chapter: 'ch3', level: 1, x: 400, y: 150 },
        { id: 'diode', name: '二极管', chapter: 'ch3', level: 1, x: 600, y: 150 },
        { id: 'special_diode', name: '特殊二极管', chapter: 'ch3', level: 1, x: 800, y: 150 },
        
        // 三极管层
        { id: 'bjt', name: 'BJT三极管', chapter: 'ch5', level: 2, x: 300, y: 280 },
        { id: 'mosfet', name: 'MOS场效应管', chapter: 'ch4', level: 2, x: 550, y: 280 },
        { id: 'jfet', name: '结型场效应管', chapter: 'ch4', level: 2, x: 750, y: 280 },
        
        // 基本放大电路层
        { id: 'ce_amp', name: '共射放大电路', chapter: 'ch5', level: 3, x: 150, y: 400 },
        { id: 'cc_amp', name: '共集放大电路', chapter: 'ch5', level: 3, x: 300, y: 400 },
        { id: 'cb_amp', name: '共基放大电路', chapter: 'ch5', level: 3, x: 450, y: 400 },
        { id: 'cs_amp', name: '共源放大电路', chapter: 'ch4', level: 3, x: 600, y: 400 },
        { id: 'cd_amp', name: '共漏放大电路', chapter: 'ch4', level: 3, x: 750, y: 400 },
        { id: 'cg_amp', name: '共栅放大电路', chapter: 'ch4', level: 3, x: 900, y: 400 },
        
        // 小信号模型
        { id: 'small_signal', name: '小信号模型分析', chapter: 'ch4', level: 3, x: 525, y: 500 },
        
        // 多级放大电路
        { id: 'multi_stage', name: '多级放大电路', chapter: 'ch5', level: 4, x: 525, y: 600 },
        
        // 模拟集成电路层
        { id: 'dc_bias', name: '直流偏置技术', chapter: 'ch7', level: 5, x: 300, y: 700 },
        { id: 'diff_amp', name: '差分放大电路', chapter: 'ch7', level: 5, x: 525, y: 700 },
        { id: 'op_amp_internal', name: '运放内部电路', chapter: 'ch7', level: 5, x: 750, y: 700 },
        
        // 运算放大器应用层
        { id: 'ideal_opamp', name: '理想运放', chapter: 'ch2', level: 6, x: 400, y: 820 },
        { id: 'linear_opamp', name: '线性运放电路', chapter: 'ch2', level: 6, x: 650, y: 820 },
        
        // 反馈层
        { id: 'feedback', name: '反馈放大电路', chapter: 'ch8', level: 7, x: 525, y: 940 },
        
        // 功率放大层
        { id: 'power_amp', name: '功率放大电路', chapter: 'ch9', level: 8, x: 300, y: 1060 },
        { id: 'class_ab', name: '甲乙类功放', chapter: 'ch9', level: 8, x: 525, y: 1060 },
        { id: 'power_ic', name: '集成功放', chapter: 'ch9', level: 8, x: 750, y: 1060 },
        
        // 信号处理层
        { id: 'filter', name: '有源滤波电路', chapter: 'ch10', level: 9, x: 300, y: 1180 },
        { id: 'oscillator', name: '正弦波振荡电路', chapter: 'ch10', level: 9, x: 525, y: 1180 },
        { id: 'signal_gen', name: '信号产生电路', chapter: 'ch10', level: 9, x: 750, y: 1180 },
        
        // 电源层
        { id: 'rectifier', name: '整流滤波电路', chapter: 'ch11', level: 10, x: 400, y: 1300 },
        { id: 'regulator', name: '稳压电路', chapter: 'ch11', level: 10, x: 650, y: 1300 }
    ],
    links: [
        // 基础 -> 半导体
        { source: 'signal', target: 'semiconductor' },
        { source: 'spectrum', target: 'semiconductor' },
        { source: 'semiconductor', target: 'pn_junction' },
        { source: 'pn_junction', target: 'diode' },
        { source: 'diode', target: 'special_diode' },
        
        // 半导体 -> 三极管
        { source: 'pn_junction', target: 'bjt' },
        { source: 'semiconductor', target: 'mosfet' },
        { source: 'semiconductor', target: 'jfet' },
        
        // 三极管 -> 放大电路
        { source: 'bjt', target: 'ce_amp' },
        { source: 'bjt', target: 'cc_amp' },
        { source: 'bjt', target: 'cb_amp' },
        { source: 'mosfet', target: 'cs_amp' },
        { source: 'mosfet', target: 'cd_amp' },
        { source: 'mosfet', target: 'cg_amp' },
        
        // 小信号模型
        { source: 'ce_amp', target: 'small_signal' },
        { source: 'cs_amp', target: 'small_signal' },
        
        // 多级放大
        { source: 'small_signal', target: 'multi_stage' },
        { source: 'ce_amp', target: 'multi_stage' },
        { source: 'cc_amp', target: 'multi_stage' },
        
        // 模拟集成电路
        { source: 'multi_stage', target: 'dc_bias' },
        { source: 'multi_stage', target: 'diff_amp' },
        { source: 'diff_amp', target: 'op_amp_internal' },
        
        // 运放应用
        { source: 'op_amp_internal', target: 'ideal_opamp' },
        { source: 'ideal_opamp', target: 'linear_opamp' },
        
        // 反馈
        { source: 'linear_opamp', target: 'feedback' },
        { source: 'multi_stage', target: 'feedback' },
        
        // 功率放大
        { source: 'cc_amp', target: 'power_amp' },
        { source: 'feedback', target: 'power_amp' },
        { source: 'power_amp', target: 'class_ab' },
        { source: 'class_ab', target: 'power_ic' },
        
        // 信号处理
        { source: 'linear_opamp', target: 'filter' },
        { source: 'filter', target: 'oscillator' },
        { source: 'feedback', target: 'oscillator' },
        { source: 'oscillator', target: 'signal_gen' },
        
        // 电源
        { source: 'diode', target: 'rectifier' },
        { source: 'special_diode', target: 'regulator' },
        { source: 'rectifier', target: 'regulator' },
        { source: 'feedback', target: 'regulator' }
    ]
};

// ============================================================
// 知识点标签体系
// ============================================================
// 双顶层结构：
//   - type: 'chapter'  章节体系（按教材章节组织）
//   - type: 'topic'    知识体系（按知识领域组织）
// 所有教学资源通过 tags 字段关联到知识点标签
// 知识图谱自动根据标签的父子关系（parent）生成节点和连线
// ============================================================

const KNOWLEDGE_TAGS = [
    // ========== 顶层：章节体系 ==========
    { id: 'root_chapter', name: '章节体系', parent: null, type: 'root', category: 'chapter' },
    
    // 第一章
    { id: 'ch1', name: '第一章 绪论', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch1-1', name: '信号', parent: 'ch1', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch1-2', name: '信号的频谱', parent: 'ch1', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['calculation', 'analysis'] },
    { id: 'ch1-3', name: '模拟信号和数字信号', parent: 'ch1', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch1-4', name: '放大电路模型', parent: 'ch1', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch1-5', name: '放大电路的主要性能指标', parent: 'ch1', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['calculation', 'analysis'] },
    
    // 第二章
    { id: 'ch2', name: '第二章 运算放大器', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch2-1', name: '集成电路运算放大器', parent: 'ch2', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch2-2', name: '理想运算放大器', parent: 'ch2', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch2-3', name: '基本线性运放电路', parent: 'ch2', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch2-4', name: '同相反相输入放大电路应用', parent: 'ch2', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    
    // 第三章
    { id: 'ch3', name: '第三章 二极管及基本电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch3-1', name: '半导体的基本知识', parent: 'ch3', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch3-2', name: 'PN结的形成及特性', parent: 'ch3', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch3-3', name: '二极管', parent: 'ch3', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch3-4', name: '二极管基本电路及分析方法', parent: 'ch3', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch3-5', name: '特殊二极管', parent: 'ch3', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    
    // 第四章
    { id: 'ch4', name: '第四章 场效应三极管及放大电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch4-1', name: 'MOS场效应三极管', parent: 'ch4', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch4-2', name: 'MOSFET基本共源放大电路', parent: 'ch4', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch4-4', name: '小信号模型分析法', parent: 'ch4', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
    { id: 'ch4-5', name: '共漏极和共栅极放大电路', parent: 'ch4', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    
    // 第五章
    { id: 'ch5', name: '第五章 双极结型三极管及放大电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch5-1', name: 'BJT三极管', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch5-2-1', name: '基本共射极放大电路', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch5-2-2', name: 'BJT放大电路图解分析', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal2'], types: ['analysis'] },
    { id: 'ch5-2-3', name: 'BJT小信号模型', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
    { id: 'ch5-2-4', name: '共射极放大电路', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch5-2-5', name: '共集电极和共基极放大电路', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch5-4', name: '多级放大电路', parent: 'ch5', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
    
    // 第七章
    { id: 'ch7', name: '第七章 模拟集成电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch7-1', name: '直流偏置技术', parent: 'ch7', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch7-2', name: '差分式放大电路', parent: 'ch7', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch7-4', name: '集成运算放大器电路简介', parent: 'ch7', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch7-5', name: '实际运放主要参数及应用', parent: 'ch7', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
    
    // 第八章
    { id: 'ch8', name: '第八章 反馈放大电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch8-1', name: '反馈的基本概念与分类', parent: 'ch8', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch8-2', name: '负反馈放大电路增益表达式', parent: 'ch8', type: 'section', category: 'chapter', objectives: ['goal2'], types: ['calculation', 'analysis'] },
    { id: 'ch8-3', name: '负反馈对放大电路性能的影响', parent: 'ch8', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
    { id: 'ch8-4', name: '深度负反馈条件下的近似计算', parent: 'ch8', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis'] },
    
    // 第九章
    { id: 'ch9', name: '第九章 功率放大电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch9-1', name: '功率放大电路的一般问题', parent: 'ch9', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch9-3', name: '乙类双电源互补对称功放', parent: 'ch9', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch9-4', name: '甲乙类互补对称功率放大电路', parent: 'ch9', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch9-6', name: '功率管', parent: 'ch9', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch9-7', name: '集成功率放大器', parent: 'ch9', type: 'section', category: 'chapter', objectives: ['goal2'], types: ['analysis', 'design'] },
    
    // 第十章
    { id: 'ch10', name: '第十章 信号处理与信号产生电路', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch10-1', name: '滤波电路基本概念与分类', parent: 'ch10', type: 'section', category: 'chapter', objectives: ['goal1'], types: ['analysis'] },
    { id: 'ch10-2', name: '一阶有源滤波电路', parent: 'ch10', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch10-5', name: '正弦波振荡电路的振荡条件', parent: 'ch10', type: 'section', category: 'chapter', objectives: ['goal1', 'goal2'], types: ['analysis'] },
    { id: 'ch10-6', name: 'RC正弦波振荡电路', parent: 'ch10', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    
    // 第十一章
    { id: 'ch11', name: '第十一章 直流稳压电源', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'ch11-1', name: '小功率整流滤波电路', parent: 'ch11', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    { id: 'ch11-2', name: '线性稳压电路', parent: 'ch11', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['calculation', 'analysis', 'design'] },
    
    // 实验
    { id: 'exp', name: '实验', parent: 'root_chapter', type: 'chapter', category: 'chapter' },
    { id: 'exp1', name: '实验一 晶体管放大电路指标测试', parent: 'exp', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
    { id: 'exp2', name: '实验二 集成运放应用电路及指标测试', parent: 'exp', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
    { id: 'exp3', name: '实验三 功率放大器指标测试', parent: 'exp', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
    { id: 'exp4', name: '实验四 信号发生器指标参数测试', parent: 'exp', type: 'section', category: 'chapter', objectives: ['goal2', 'goal3'], types: ['analysis', 'design'] },
    
    // ========== 顶层：知识体系 ==========
    { id: 'root_topic', name: '知识体系', parent: null, type: 'root', category: 'topic' },
    
    // 基础概念
    { id: 't_basic', name: '基础概念', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_signal', name: '信号与频谱', parent: 't_basic', type: 'knowledge', category: 'topic' },
    { id: 't_amp_model', name: '放大电路模型与指标', parent: 't_basic', type: 'knowledge', category: 'topic' },
    
    // 半导体器件
    { id: 't_semi', name: '半导体器件', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_semi_basic', name: '半导体基础', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_pn', name: 'PN结', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_diode', name: '二极管', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_special_diode', name: '特殊二极管', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_bjt', name: 'BJT三极管', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_mosfet', name: 'MOS场效应管', parent: 't_semi', type: 'knowledge', category: 'topic' },
    { id: 't_jfet', name: '结型场效应管', parent: 't_semi', type: 'knowledge', category: 'topic' },
    
    // 基本放大电路
    { id: 't_basic_amp', name: '基本放大电路', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_ce_amp', name: '共射放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_cc_amp', name: '共集放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_cb_amp', name: '共基放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_cs_amp', name: '共源放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_cd_amp', name: '共漏放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_cg_amp', name: '共栅放大电路', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    { id: 't_small_signal', name: '小信号模型分析', parent: 't_basic_amp', type: 'knowledge', category: 'topic' },
    
    // 多级放大
    { id: 't_multi', name: '多级放大电路', parent: 'root_topic', type: 'topic', category: 'topic' },
    
    // 模拟集成电路
    { id: 't_analog_ic', name: '模拟集成电路', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_dc_bias', name: '直流偏置技术', parent: 't_analog_ic', type: 'knowledge', category: 'topic' },
    { id: 't_diff_amp', name: '差分放大电路', parent: 't_analog_ic', type: 'knowledge', category: 'topic' },
    { id: 't_opamp_internal', name: '运放内部电路', parent: 't_analog_ic', type: 'knowledge', category: 'topic' },
    
    // 运放应用
    { id: 't_opamp_app', name: '运算放大器应用', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_ideal_opamp', name: '理想运放', parent: 't_opamp_app', type: 'knowledge', category: 'topic' },
    { id: 't_linear_opamp', name: '线性运放电路', parent: 't_opamp_app', type: 'knowledge', category: 'topic' },
    
    // 反馈电路
    { id: 't_feedback', name: '反馈放大电路', parent: 'root_topic', type: 'topic', category: 'topic' },
    
    // 功率放大
    { id: 't_power', name: '功率放大电路', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_class_ab', name: '甲乙类功放', parent: 't_power', type: 'knowledge', category: 'topic' },
    { id: 't_power_ic', name: '集成功放', parent: 't_power', type: 'knowledge', category: 'topic' },
    
    // 信号处理
    { id: 't_signal_proc', name: '信号处理与产生', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_filter', name: '有源滤波电路', parent: 't_signal_proc', type: 'knowledge', category: 'topic' },
    { id: 't_oscillator', name: '正弦波振荡电路', parent: 't_signal_proc', type: 'knowledge', category: 'topic' },
    { id: 't_signal_gen', name: '信号产生电路', parent: 't_signal_proc', type: 'knowledge', category: 'topic' },
    
    // 直流电源
    { id: 't_power_supply', name: '直流稳压电源', parent: 'root_topic', type: 'topic', category: 'topic' },
    { id: 't_rectifier', name: '整流滤波电路', parent: 't_power_supply', type: 'knowledge', category: 'topic' },
    { id: 't_regulator', name: '稳压电路', parent: 't_power_supply', type: 'knowledge', category: 'topic' }
];

// 知识点分类颜色（知识体系的层级颜色）
const TOPIC_LEVEL_COLORS = {
    0: '#3b82f6', // 顶层根节点
    1: '#8b5cf6', // 一级分类
    2: '#ec4899', // 二级分类/知识点
    3: '#f59e0b',
    4: '#10b981'
};

const TOPIC_CATEGORY_COLORS = {
    '基础概念': '#3b82f6',
    '半导体器件': '#8b5cf6',
    '基本放大电路': '#f59e0b',
    '多级放大电路': '#f97316',
    '模拟集成电路': '#10b981',
    '运算放大器应用': '#06b6d4',
    '反馈放大电路': '#6366f1',
    '功率放大电路': '#ef4444',
    '信号处理与产生': '#eab308',
    '直流稳压电源': '#14b8a6'
};

// 章节颜色（每章一个颜色）
const CHAPTER_COLORS = {
    'ch1': '#64748b',
    'ch2': '#3b82f6',
    'ch3': '#8b5cf6',
    'ch4': '#ec4899',
    'ch5': '#f59e0b',
    'ch7': '#10b981',
    'ch8': '#6366f1',
    'ch9': '#ef4444',
    'ch10': '#eab308',
    'ch11': '#14b8a6',
    'exp': '#64748b'
};

/**
 * 根据知识点标签体系自动生成图谱数据
 * @param {string} category - 'topic' 知识体系 或 'chapter' 章节体系
 * @returns {object} { nodes, links }
 */
function generateGraphFromTags(category) {
    const nodes = [];
    const links = [];
    
    // 筛选该分类下的所有标签
    const categoryTags = KNOWLEDGE_TAGS.filter(t => t.category === category);
    
    // 计算每个标签的深度层级
    const depthMap = new Map();
    function getDepth(tagId) {
        if (depthMap.has(tagId)) return depthMap.get(tagId);
        const tag = KNOWLEDGE_TAGS.find(t => t.id === tagId);
        if (!tag || !tag.parent) {
            depthMap.set(tagId, 0);
            return 0;
        }
        const d = getDepth(tag.parent) + 1;
        depthMap.set(tagId, d);
        return d;
    }
    
    // 计算子节点数量（用于节点大小）
    const childCountMap = new Map();
    KNOWLEDGE_TAGS.forEach(t => {
        if (t.parent) {
            childCountMap.set(t.parent, (childCountMap.get(t.parent) || 0) + 1);
        }
    });
    
    categoryTags.forEach(tag => {
        const depth = getDepth(tag.id);
        const childCount = childCountMap.get(tag.id) || 0;
        
        // 确定颜色
        let color;
        if (category === 'topic') {
            // 知识体系：按一级分类着色
            // 找到一级分类祖先
            let ancestor = tag;
            while (ancestor.parent && ancestor.parent !== 'root_topic') {
                ancestor = KNOWLEDGE_TAGS.find(t => t.id === ancestor.parent);
            }
            color = TOPIC_CATEGORY_COLORS[ancestor.name] || '#64748b';
        } else {
            // 章节体系：按章节着色
            let chapterId = tag.id;
            if (tag.type === 'section') {
                chapterId = tag.parent;
            }
            color = CHAPTER_COLORS[chapterId] || '#64748b';
        }
        
        nodes.push({
            id: tag.id,
            name: tag.name,
            level: depth,
            category: category,
            tagType: tag.type,
            childCount: childCount,
            color: color,
            objectives: tag.objectives || [],
            types: tag.types || []
        });
        
        // 连线（父子关系）
        if (tag.parent) {
            const parentTag = KNOWLEDGE_TAGS.find(t => t.id === tag.parent);
            if (parentTag && parentTag.category === category) {
                links.push({
                    source: tag.parent,
                    target: tag.id
                });
            }
        }
    });
    
    return { nodes, links };
}

/**
 * 同时生成章节体系和知识体系的双图数据
 * 两张图之间通过交叉关联（同一知识点同时属于某章节和某知识领域）连接
 */
function generateCombinedGraph() {
    const topicGraph = generateGraphFromTags('topic');
    const chapterGraph = generateGraphFromTags('chapter');
    
    // 合并节点
    const allNodes = [...chapterGraph.nodes, ...topicGraph.nodes];
    const allLinks = [...chapterGraph.links, ...topicGraph.links];
    
    return {
        nodes: allNodes,
        links: allLinks,
        chapterNodes: chapterGraph.nodes,
        topicNodes: topicGraph.nodes
    };
}

// ============================================================
// 专题导航体系
// ============================================================

// 五大核心放大电路
const CORE_CIRCUITS = [
    {
        id: 'linear_opamp',
        name: '线性运算放大电路',
        shortName: '运算放大',
        icon: '🔺',
        color: '#3b82f6',
        description: '由集成运放构成的线性放大电路，包括反相比例、同相比例、求和、差分等基本运算电路',
        tagIds: ['ch2-3', 'ch2-4', 't_linear_opamp'],
        questionTypes: ['calculation', 'analysis', 'design'],
        isKey: true,
        isDifficult: false,
        designFocus: true,
        learning: [
            { id: 'lin-l1', name: '同相放大电路', desc: '输入从同相端引入，电压增益由反馈网络决定', lab: 'interactive/lin-l1.html' },
            { id: 'lin-l2', name: '电压跟随器', desc: '同相放大电路的特例，增益为 1，用于阻抗变换' },
            { id: 'lin-l3', name: '反相放大电路', desc: '虚地概念与反相比例运算电路的分析' },
            { id: 'lin-l4', name: '求差电路', desc: '对两个输入信号之差进行放大的差分运算电路' },
            { id: 'lin-l5', name: '仪用放大电路', desc: '三运放高输入阻抗结构，广泛用于弱信号测量' },
            { id: 'lin-l6', name: '求和电路', desc: '反相求和与同相求和电路的组成与系数计算' },
            { id: 'lin-l7', name: '微积分电路', desc: '积分与微分运算电路的原理及输入输出关系' }
        ],
        training: [
            { id: 'lin-t1', name: '同相放大训练', desc: '同相比例电路增益与输入输出关系计算' },
            { id: 'lin-t2', name: '反相放大训练', desc: '反相比例电路的分析与参数设计' },
            { id: 'lin-t3', name: '求和运算放大训练', desc: '多路信号加权求和电路的计算练习' },
            { id: 'lin-t4', name: '多级运算放大训练', desc: '两级级联（同相＋反相）电压放大倍数分级计算', lab: 'interactive/lin-t4.html' }
        ]
    },
    {
        id: 'ce_amp',
        name: '共射放大电路',
        shortName: '共射放大',
        icon: '🔷',
        color: '#f59e0b',
        description: 'BJT共射极放大电路，模电最核心的放大电路形式，涉及静态分析、动态分析、图解法和小信号模型',
        tagIds: ['ch5-2-1', 'ch5-2-3', 'ch5-2-4', 't_ce_amp'],
        questionTypes: ['calculation', 'analysis', 'design'],
        isKey: true,
        isDifficult: true,
        learning: [
            { id: 'ce-l1', name: '基本共射极放大电路', desc: '电路组成、放大原理与各元件的作用' },
            { id: 'ce-l2', name: '直流静态分析', desc: '直流通路估算静态工作点 Q（IBQ、ICQ、UCEQ）' },
            { id: 'ce-l3', name: '图解分析法', desc: '负载线与 Q 点的图解，波形失真分析' },
            { id: 'ce-l4', name: 'BJT 小信号模型', desc: 'h 参数等效模型与动态参数分析' },
            { id: 'ce-l5', name: '静态工作点稳定电路', desc: '分压式偏置电路稳定 Q 点的原理' }
        ],
        training: [
            { id: 'ce-t1', name: '静态工作点计算训练', desc: '直流通路 Q 点估算专项练习' },
            { id: 'ce-t2', name: '动态参数计算训练', desc: 'Au、Ri、Ro 的微变等效电路计算' },
            { id: 'ce-t3', name: '图解法应用训练', desc: '作图求 Q 点与非线性失真判断' },
            { id: 'ce-t4', name: '小信号模型分析训练', desc: '小信号等效电路建模与求解练习' }
        ]
    },
    {
        id: 'cs_amp',
        name: '共源放大电路',
        shortName: '共源放大',
        icon: '🔶',
        color: '#ec4899',
        description: 'MOSFET共源极放大电路，场效应管放大电路的核心形式',
        tagIds: ['ch4-2', 'ch4-4', 't_cs_amp'],
        questionTypes: ['calculation', 'analysis', 'design'],
        isKey: true,
        isDifficult: true,
        learning: [
            { id: 'cs-l1', name: 'MOSFET 共源放大电路', desc: '电路组成、自偏压与分压式偏置' },
            { id: 'cs-l2', name: '静态工作点分析', desc: '增强型/耗尽型 MOSFET 的 Q 点求解' },
            { id: 'cs-l3', name: '小信号模型分析', desc: '跨导 gm 及 Au、Ri、Ro 的计算' },
            { id: 'cs-l4', name: '共漏极放大电路', desc: '源极跟随器的特点与应用' },
            { id: 'cs-l5', name: '共栅极放大电路', desc: '电路结构与高频特性特点' }
        ],
        training: [
            { id: 'cs-t1', name: '共源静态分析训练', desc: '偏置电路 Q 点计算专项练习' },
            { id: 'cs-t2', name: '共源动态计算训练', desc: 'gm 与增益、输入输出电阻计算' },
            { id: 'cs-t3', name: '小信号模型应用训练', desc: 'FET 小信号等效电路建模练习' }
        ]
    },
    {
        id: 'diff_amp',
        name: '差分放大电路',
        shortName: '差分放大',
        icon: '⚡',
        color: '#10b981',
        description: '差分式放大电路，集成运放的核心输入级，具有抑制共模信号的特性',
        tagIds: ['ch7-2', 't_diff_amp'],
        questionTypes: ['calculation', 'analysis', 'design'],
        isKey: true,
        isDifficult: true,
        learning: [
            { id: 'diff-l1', name: '差分放大电路的组成', desc: '对称结构与抑制零点漂移的原理' },
            { id: 'diff-l2', name: '差模信号与共模信号', desc: '两类信号的定义、分解与处理' },
            { id: 'diff-l3', name: '共模抑制比', desc: 'KCMR 的定义、意义与提高途径' },
            { id: 'diff-l4', name: '恒流源差分电路', desc: '用恒流源取代 Re 提高共模抑制能力' },
            { id: 'diff-l5', name: '输入输出方式', desc: '双端/单端输入、双端/单端输出的组合分析' }
        ],
        training: [
            { id: 'diff-t1', name: '差模增益计算训练', desc: '差模放大倍数与输入输出电阻计算' },
            { id: 'diff-t2', name: '共模抑制比分析训练', desc: 'KCMR 计算与电路改进分析' },
            { id: 'diff-t3', name: '恒流源电路分析训练', desc: '含恒流源差分电路的综合练习' }
        ]
    },
    {
        id: 'power_amp',
        name: '功率放大电路',
        shortName: '功率放大',
        icon: '🔋',
        color: '#ef4444',
        description: '功率放大电路，包括乙类和甲乙类互补对称电路，关注输出功率和效率',
        tagIds: ['ch9-1', 'ch9-3', 'ch9-4', 't_class_ab', 't_power_ic'],
        questionTypes: ['calculation', 'analysis', 'design'],
        isKey: true,
        isDifficult: false,
        designFocus: true,
        learning: [
            { id: 'pa-l1', name: '功率放大电路的特点', desc: '与大信号放大、效率与失真的矛盾' },
            { id: 'pa-l2', name: '乙类互补对称功放', desc: 'OCL 电路组成与工作原理' },
            { id: 'pa-l3', name: '交越失真', desc: '失真产生的原因与消除方法' },
            { id: 'pa-l4', name: '甲乙类互补对称功放', desc: '偏置电路设置与性能分析' },
            { id: 'pa-l5', name: '集成功率放大器', desc: '典型集成功放的引脚与应用电路' }
        ],
        training: [
            { id: 'pa-t1', name: '输出功率与效率训练', desc: 'Pom、PV、效率 η 的计算练习' },
            { id: 'pa-t2', name: '功率管选择训练', desc: '管耗估算与极限参数校核' },
            { id: 'pa-t3', name: '功放电路设计训练', desc: '给定指标下的功放电路参数设计' }
        ]
    }
];

// 游戏闯关主题（首页游戏闯关模块）
const GAME_TOPICS = [
    { id: 'game_linear_opamp', name: '运算放大', circuitId: 'linear_opamp' },
    { id: 'game_ce_amp', name: '共射放大', circuitId: 'ce_amp' },
    { id: 'game_cs_amp', name: '共源放大', circuitId: 'cs_amp' },
    { id: 'game_diff_amp', name: '差分放大', circuitId: 'diff_amp' },
    { id: 'game_power_amp', name: '功率放大', circuitId: 'power_amp' },
    { id: 'game_regulator', name: '直流稳压电源', color: '#14b8a6', icon: '⚡' }
];

// 分支电路与案例数据（游戏闯关 / 题型解析专题页用）
// thumb: 缩略图样式（noninv 同相 / inv 反相 / sum 求和 / diff 求差 / multi 多级 / generic 通用）
// cases.game 游戏闯关案例；cases.calculation 计算题型解析案例；cases.design 设计题型解析案例
// 案例字段：name 案例名、desc 说明、lab 交互电路页（有则可点击进入）、ready 是否已制作
// thumbImg：真实页面截图缩略图（仅已建案例使用，如 assets/thumb-lin-l1.png）；未建案例仍用 branch.thumb 简笔示意
const CIRCUIT_BRANCHES = {
    linear_opamp: [
        {
            id: 'lin-b1', name: '同相放大', thumb: 'noninv',
            desc: '输入从同相端引入，电压增益 1 + Rf/R1',
            cases: {
                game: [
                    { name: '关卡1 · 识别放大类型', desc: '观察电路判断同相/反相' },
                    { name: '关卡2 · 计算电压增益', desc: '拖动电阻值使增益达标' }
                ],
                calculation: [
                    { name: '案例1 · 同相放大电路分析', desc: '虚短虚断推导电压增益 Av', lab: 'interactive/lin-l1.html', ready: true, thumbImg: 'assets/thumb-lin-l1.png' },
                    { name: '案例2 · 平衡电阻的作用', desc: '分析 R3 = R1∥R2 的取值依据' }
                ],
                design: [
                    { name: '设计1 · 指定增益电路设计', desc: '按 Av=11 选取反馈电阻' }
                ]
            }
        },
        {
            id: 'lin-b2', name: '反相放大', thumb: 'inv',
            desc: '输入从反相端引入，增益 −Rf/R1',
            cases: {
                game: [
                    { name: '关卡1 · 反相放大识别', desc: '判断相位关系' }
                ],
                calculation: [
                    { name: '案例1 · 反相放大电路分析', desc: '推导 Av = −R2/R1' },
                    { name: '案例2 · 输入电阻计算', desc: '分析 Ri = R1 的原因' }
                ],
                design: []
            }
        },
        {
            id: 'lin-b3', name: '求和电路', thumb: 'sum',
            desc: '多路输入信号的加法运算',
            cases: {
                game: [
                    { name: '关卡1 · 求和电路连线', desc: '补全输入支路' },
                    { name: '关卡2 · 输出表达式', desc: '写出 Vo 表达式' }
                ],
                calculation: [
                    { name: '案例1 · 反相加法器', desc: '多路反相输入的叠加' },
                    { name: '案例2 · 同相加法器', desc: '同相端多路输入的叠加' },
                    { name: '案例3 · 加减运算电路', desc: '双端输入的加减运算' }
                ],
                design: []
            }
        },
        {
            id: 'lin-b4', name: '求差电路', thumb: 'diff',
            desc: '两路输入之差的比例运算',
            cases: {
                game: [
                    { name: '关卡1 · 求差电路识别', desc: '找出两路输入的位置' }
                ],
                calculation: [
                    { name: '案例1 · 差分输入运算电路', desc: '推导 Vo 与两路输入的关系' },
                    { name: '案例2 · 共模抑制分析', desc: '分析电阻匹配的影响' }
                ],
                design: [
                    { name: '设计1 · 求差电路参数设计', desc: '确定四个电阻取值' }
                ]
            }
        },
        {
            id: 'lin-b5', name: '多级运算放大', thumb: 'multi',
            desc: '多级级联，总增益为各级之积',
            cases: {
                game: [
                    { name: '案例1 · 电路闯关挑战（100分）', desc: '判类型 → 选框架 → 填表达式', lab: 'interactive/lin-g1.html', ready: true, thumbImg: 'assets/thumb-lin-g1.png' },
                    { name: '案例2 · 电路闯关挑战（100分）', desc: '反相求和＋反相级联，写出 Vₒ 表达式', lab: 'interactive/lin-g2.html', ready: true, thumbImg: 'assets/thumb-lin-g2.png' },
                    { name: '案例3 · 电路闯关挑战（100分）', desc: '跟随器＋反相比例（R₁=1k，R₂=10k），写出 Vₒ 表达式', lab: 'interactive/lin-g3.html', ready: true, thumbImg: 'assets/thumb-lin-g3.png' },
                    { name: '案例4 · 电路闯关挑战（100分）', desc: '同相（带分压）＋反相级联，写出 Vₒ 表达式', lab: 'interactive/lin-g4.html', ready: true, thumbImg: 'assets/thumb-lin-g4.png' }
                ],
                calculation: [
                    { name: '案例1 · 两级级联放大电路', desc: '同相＋反相级联计算 Au', lab: 'interactive/lin-t4.html', ready: true, thumbImg: 'assets/thumb-lin-t4.png' }
                ],
                design: [
                    { name: '设计1 · 多级运算放大设计', desc: '按总增益分配各级增益' }
                ]
            }
        }
    ],
    ce_amp: [
        { id: 'ce-b1', name: '固定式偏压共射放大电路', thumb: 'generic', desc: '仅由基极偏置电阻设定静态工作点', cases: { game: [], calculation: [], design: [] } },
        { id: 'ce-b2', name: '分压式偏置共射放大电路', thumb: 'generic', desc: '稳定静态工作点的偏置方式', cases: { game: [
                    { name: '案例1 · 电路闯关挑战（100分）', desc: '求 Q 点（IBQ/ICQ/VCEQ）与 Av/Ri/Ro 表达式', lab: 'interactive/cj-g1.html?v=43', ready: true, thumbImg: 'assets/thumb-cj-g1.png' }
                ], calculation: [], design: [] } },
        { id: 'ce-b3', name: '双电源共射放大电路', thumb: 'multi', desc: '正负双电源供电的共射放大电路', cases: { game: [], calculation: [], design: [] } }
    ],
    cs_amp: [
        { id: 'cs-b1', name: '共源放大电路', thumb: 'generic', desc: 'MOSFET 共源放大电路', cases: { game: [], calculation: [], design: [] } },
        { id: 'cs-b2', name: '共漏放大电路', thumb: 'generic', desc: '源极跟随器', cases: { game: [], calculation: [], design: [] } },
        { id: 'cs-b3', name: '共栅放大电路', thumb: 'generic', desc: '共栅极组态放大电路', cases: { game: [], calculation: [], design: [] } }
    ],
    diff_amp: [
        { id: 'df-b1', name: '长尾式差分放大电路', thumb: 'diff', desc: '典型差分放大电路结构', cases: { game: [], calculation: [], design: [] } },
        { id: 'df-b2', name: '镜像电流源电路', thumb: 'generic', desc: '电流源偏置电路', cases: { game: [], calculation: [], design: [] } },
        { id: 'df-b3', name: '恒流源差分电路', thumb: 'diff', desc: '恒流源代替长尾电阻', cases: { game: [], calculation: [], design: [] } }
    ],
    power_amp: [
        { id: 'pa-b1', name: 'OCL功率放大电路', thumb: 'generic', desc: '无输出电容的互补对称电路', cases: { game: [], calculation: [], design: [] } },
        { id: 'pa-b2', name: 'OTL功率放大电路', thumb: 'generic', desc: '无输出变压器的功放电路', cases: { game: [], calculation: [], design: [] } },
        { id: 'pa-b3', name: '集成功率放大器', thumb: 'generic', desc: '集成芯片构成的功放', cases: { game: [], calculation: [], design: [] } }
    ],
    regulator: [
        { id: 'rg-b1', name: '整流电路', thumb: 'generic', desc: '单向/桥式整流电路', cases: { game: [], calculation: [], design: [] } },
        { id: 'rg-b2', name: '滤波电路', thumb: 'generic', desc: '电容/电感滤波', cases: { game: [], calculation: [], design: [] } },
        { id: 'rg-b3', name: '串联型稳压电路', thumb: 'generic', desc: '串联调整管稳压', cases: { game: [], calculation: [], design: [] } },
        { id: 'rg-b4', name: '开关型稳压电路', thumb: 'generic', desc: '开关电源基本原理', cases: { game: [], calculation: [], design: [] } }
    ]
};

// 题型分类关联的知识点
const QUESTION_TYPE_TOPICS = {
    calculation: [
        { circuitId: 'linear_opamp', name: '运算放大' },
        { circuitId: 'ce_amp', name: '共射放大' },
        { circuitId: 'cs_amp', name: '共源放大' },
        { circuitId: 'diff_amp', name: '差分放大' },
        { circuitId: 'power_amp', name: '功率放大' }
    ],
    design: [
        { circuitId: 'linear_opamp', name: '运算放大' },
        { circuitId: 'power_amp', name: '功率放大' },
        { name: '直流稳压电源', color: '#14b8a6', icon: '⚡', tagIds: ['ch11-1', 'ch11-2', 't_regulator'] }
    ],
    analysis: [
        { circuitId: 'linear_opamp', name: '运算放大' },
        { circuitId: 'ce_amp', name: '共射放大' },
        { circuitId: 'cs_amp', name: '共源放大' },
        { circuitId: 'diff_amp', name: '差分放大' },
        { circuitId: 'power_amp', name: '功率放大' }
    ]
};

// 专题导航分类
const FOCUS_CATEGORIES = [
    { id: 'core_circuits', name: '核心放大电路', icon: '⚡', description: '五大核心放大电路——模电最重要内容', color: '#6366f1' },
    { id: 'key_content', name: '重点内容', icon: '⭐', description: '课程要求重点掌握的知识点', color: '#f59e0b' },
    { id: 'difficult', name: '难点内容', icon: '🔥', description: '学习难度较大的知识点', color: '#ef4444' },
    { id: 'calculation', name: '计算题型', icon: '🧮', description: '涉及定量计算的知识点', color: '#e74c3c' },
    { id: 'analysis', name: '分析题型', icon: '📊', description: '涉及电路分析的知识点', color: '#3498db' },
    { id: 'design', name: '设计题型', icon: '🎨', description: '涉及电路设计的知识点', color: '#2ecc71' }
];

// 重点知识点标签ID（核心电路之外）
const KEY_CONTENT_TAG_IDS = [
    'ch1-5',   'ch2-2',   'ch5-2-3', 'ch8-1',   'ch8-3',
    'ch10-5',  'ch10-6',  'ch11-1',  'ch11-2',
    't_small_signal', 't_feedback', 't_filter', 't_oscillator', 't_ideal_opamp'
];

// 难点知识点标签ID
const DIFFICULT_TAG_IDS = [
    'ch3-2',   'ch5-2-2', 'ch5-2-3', 'ch7-2',   'ch8-1',
    'ch8-4',   'ch4-4',
    't_diff_amp', 't_small_signal', 't_feedback'
];

// 根据专题分类获取相关标签
function getTagsByFocusCategory(categoryId) {
    if (categoryId === 'core_circuits') {
        const ids = new Set();
        CORE_CIRCUITS.forEach(c => c.tagIds.forEach(id => ids.add(id)));
        return KNOWLEDGE_TAGS.filter(t => ids.has(t.id));
    }
    if (categoryId === 'key_content') {
        const ids = new Set(KEY_CONTENT_TAG_IDS);
        CORE_CIRCUITS.forEach(c => c.tagIds.forEach(id => ids.add(id)));
        return KNOWLEDGE_TAGS.filter(t => ids.has(t.id));
    }
    if (categoryId === 'difficult') {
        const ids = new Set(DIFFICULT_TAG_IDS);
        return KNOWLEDGE_TAGS.filter(t => ids.has(t.id));
    }
    if (['calculation', 'analysis', 'design'].includes(categoryId)) {
        return KNOWLEDGE_TAGS.filter(t => t.types && t.types.includes(categoryId));
    }
    return [];
}

// 根据标签ID找到对应的章节信息
function getChapterInfoByTagId(tagId) {
    const tag = KNOWLEDGE_TAGS.find(t => t.id === tagId);
    if (!tag) return null;
    
    if (tag.category === 'chapter') {
        if (tag.type === 'section') {
            const chapterTag = KNOWLEDGE_TAGS.find(t => t.id === tag.parent);
            return { chapter: chapterTag ? chapterTag.name : '', section: tag.name };
        }
        return { chapter: tag.name, section: '' };
    }
    
    // topic类型：找关联的章节
    return { chapter: '', section: tag.name, topic: true };
}
