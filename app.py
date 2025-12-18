import streamlit as st
import pandas as pd
import random
import time

# ==========================================
# 1. 核心配置：关键词映射数据库 (Mapping Database)
# 键：平台名称 | 值：{风格标签: {维度: 关键词}}
# ==========================================
DB_MAPPING = {
    "Musicbed": {
        "开心/俏皮": {"Mood": "Whimsical, Carefree, Playful", "Genre": "Indie Pop, World", "Attr": "Bright, Quirky"},
        "史诗/电影感": {"Mood": "Cinematic, Euphoric, Anthemic", "Genre": "Score, Orchestral", "Attr": "Build, Wide"},
        "放松/生活": {"Mood": "Relaxed, Intimate, Chill", "Genre": "Folk, Acoustic", "Attr": "Earthy, Organic"},
        "科技/商业": {"Mood": "Driving, Confident", "Genre": "Electronic, Pop", "Attr": "Minimal, Tech"}
    },
    "Artlist": {
        "开心/俏皮": {"Theme": "Vlog, Kids", "Mood": "Happy, Uplifting", "Genre": "Acoustic, Pop"},
        "史诗/电影感": {"Theme": "Film, Trailer", "Mood": "Powerful, Serious", "Genre": "Cinematic"},
        "放松/生活": {"Theme": "Lifestyle, Food", "Mood": "Peaceful, Love", "Genre": "Acoustic, Folk"},
        "科技/商业": {"Theme": "Technology, Business", "Mood": "Corporate, Motivation", "Genre": "Electronic"}
    },
    "PremiumBeat": {
        "开心/俏皮": {"Genre": "Comedy / Cartoons", "Mood": "Positive, Happy", "Sub": "Childlike"},
        "史诗/电影感": {"Genre": "Production Music", "Mood": "Adventure, Dramatic", "Sub": "Trailer"},
        "放松/生活": {"Genre": "Easy Listening", "Mood": "Relaxing, Romantic", "Sub": "Acoustic"},
        "科技/商业": {"Genre": "Corporate", "Mood": "Motivational, Driving", "Sub": "Tech"}
    }
}

# ==========================================
# 2. 页面基础配置 (Page Configuration)
# ==========================================
st.set_page_config(
    page_title="SyncMatch - 配乐关键词助手",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"  # 侧边栏默认展开
)

# 自定义样式（优化视觉体验）
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4F46E5;
        color: white;
    }
    .stCode {
        border-radius: 6px;
        background-color: #F8F9FA;
    }
    .metric-container {
        padding: 10px;
        border-radius: 8px;
        background-color: #EFF6FF;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 页面标题与说明 (Title & Description)
# ==========================================
st.title("🎵 SyncMatch - 视频配乐关键词生成器")
st.markdown("""
    上传参考视频/音频文件，自动分析风格并生成 **Musicbed、Artlist、PremiumBeat** 三大配乐平台的专属搜索关键词，
    一键直达搜索结果，提升配乐查找效率！
""")
st.divider()  # 分隔线

# ==========================================
# 4. 侧边栏：文件上传与模拟AI分析 (Sidebar: Upload & AI Analysis)
# ==========================================
with st.sidebar:
    st.header("📤 上传与分析")
    uploaded_file = st.file_uploader(
        "拖入视频/音频文件",
        type=["mp4", "mov", "mp3", "wav"],
        help="支持常见视频/音频格式，文件大小建议不超过100MB"
    )

    detected_vibe = None  # 初始化识别的风格
    mock_bpm = None       # 初始化模拟BPM

    if uploaded_file is not None:
        # 显示文件信息
        st.success(f"✅ 已加载文件：{uploaded_file.name}")
        st.markdown(f"📁 文件类型：{uploaded_file.type}")
        st.markdown("---")
        
        # 模拟AI分析进度
        st.write("🤖 AI 正在分析音频特征...")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.005)  # 缩短加载时间，提升体验
            progress_bar.progress(i + 1)
        
        # 人工确认AI识别结果（模拟真实场景的人工校验）
        st.subheader("🎯 AI 初步识别结果")
        detected_vibe = st.radio(
            "请确认音频风格（AI识别仅供参考）",
            options=["开心/俏皮", "放松/生活", "史诗/电影感", "科技/商业"],
            index=0,
            help="选择最贴合的风格标签"
        )
        
        # 模拟生成BPM（随机但更贴合风格）
        bpm_ranges = {
            "开心/俏皮": (100, 140),
            "放松/生活": (70, 90),
            "史诗/电影感": (80, 110),
            "科技/商业": (90, 130)
        }
        min_bpm, max_bpm = bpm_ranges[detected_vibe]
        mock_bpm = random.randint(min_bpm, max_bpm)
        
        # 显示BPM指标
        st.markdown("---")
        st.subheader("📊 音频特征")
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("预估 BPM（节拍/分钟）", value=f"{mock_bpm} BPM")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 主界面：生成并展示关键词结果 (Main: Result Display)
# ==========================================
if detected_vibe:
    # 结果标题
    st.header(f"🎹 分析报告：{detected_vibe}", divider="violet")
    st.info("💡 提示：点击代码块右上角「复制」按钮，可直接复制关键词；点击平台按钮直达搜索页。")
    
    # 分栏展示三个平台的结果
    col1, col2, col3 = st.columns(3, gap="medium")

    # ------------------------------
    # 平台1：Musicbed
    # ------------------------------
    with col1:
        st.subheader("🟧 Musicbed", divider="orange")
        musicbed_data = DB_MAPPING["Musicbed"][detected_vibe]
        
        # 展示关键词
        st.markdown("**🔍 搜索标签：**")
        musicbed_code = f"Mood: {musicbed_data['Mood']}\nGenre: {musicbed_data['Genre']}\nAttr: {musicbed_data['Attr']}"
        st.code(musicbed_code, language="text")
        
        # 生成搜索链接（取第一个关键词组合）
        base_query = f"{musicbed_data['Mood'].split(',')[0].strip()} {musicbed_data['Genre'].split(',')[0].strip()}"
        musicbed_url = f"https://www.musicbed.com/search?q={base_query.replace(' ', '%20')}"
        st.link_button("🚀 前往 Musicbed 搜索", url=musicbed_url, use_container_width=True)

    # ------------------------------
    # 平台2：Artlist
    # ------------------------------
    with col2:
        st.subheader("🟨 Artlist", divider="yellow")
        artlist_data = DB_MAPPING["Artlist"][detected_vibe]
        
        # 展示关键词
        st.markdown("**🔍 搜索标签：**")
        artlist_code = f"Video Theme: {artlist_data['Theme']}\nMood: {artlist_data['Mood']}\nGenre: {artlist_data['Genre']}"
        st.code(artlist_code, language="text")
        
        # 生成搜索链接
        base_query = f"{artlist_data['Mood'].split(',')[0].strip()} {artlist_data['Genre'].split(',')[0].strip()}"
        artlist_url = f"https://artlist.io/royalty-free-music/search?term={base_query.replace(' ', '%20')}"
        st.link_button("🚀 前往 Artlist 搜索", url=artlist_url, use_container_width=True)

    # ------------------------------
    # 平台3：PremiumBeat
    # ------------------------------
    with col3:
        st.subheader("🟦 PremiumBeat", divider="blue")
        premiumbeat_data = DB_MAPPING["PremiumBeat"][detected_vibe]
        
        # 展示关键词
        st.markdown("**🔍 搜索标签：**")
        premiumbeat_code = f"Genre: {premiumbeat_data['Genre']}\nMood: {premiumbeat_data['Mood']}\nSub: {premiumbeat_data['Sub']}"
        st.code(premiumbeat_code, language="text")
        
        # 生成搜索链接
        base_query = f"{premiumbeat_data['Genre'].strip()} {premiumbeat_data['Mood'].split(',')[0].strip()}"
        premiumbeat_url = f"https://www.premiumbeat.com/royalty-free-music?q={base_query.replace(' ', '%20')}"
        st.link_button("🚀 前往 PremiumBeat 搜索", url=premiumbeat_url, use_container_width=True)

else:
    # 初始状态：未上传文件时的引导界面
    st.markdown("### 👈 请在左侧侧边栏完成以下操作：")
    st.markdown("""
        1. 上传视频/音频文件（支持MP4/MOV/MP3/WAV）
        2. 等待AI分析音频特征（模拟过程）
        3. 确认AI识别的风格标签
        4. 查看并使用生成的平台专属关键词
    """)
    
    # 功能亮点展示
    st.markdown("### ✨ 核心功能")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            **🎯 精准风格识别**
            模拟AI分析音频指纹，匹配4大类核心风格
        """)
    with col2:
        st.markdown("""
            **🔤 平台专属关键词**
            针对3大配乐平台定制化生成搜索标签
        """)
    with col3:
        st.markdown("""
            **🚀 一键直达搜索**
            生成平台搜索链接，无需手动输入关键词
        """)
