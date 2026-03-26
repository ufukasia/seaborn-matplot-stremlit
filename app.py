import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

# ─── Sayfa Yapılandırması ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Matplotlib vs Seaborn | Veri Görselleştirme Dersi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0f0f1a; }
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg,#0f0f1a 0%,#1a1a2e 50%,#16213e 100%); }
[data-testid="stSidebar"] { background: #12122a !important; border-right: 1px solid #2d2d5a; }

.hero-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    border-radius: 20px; padding: 40px 36px; margin-bottom: 28px;
    box-shadow: 0 20px 60px rgba(102,126,234,.4);
}
.hero-card h1 { font-size:2.6rem; font-weight:900; color:#fff; margin:0 0 8px; }
.hero-card p  { color:rgba(255,255,255,.85); font-size:1.1rem; margin:0; }

.section-badge {
    display:inline-block; background:linear-gradient(90deg,#667eea,#764ba2);
    color:#fff; padding:4px 18px; border-radius:20px; font-size:.8rem;
    font-weight:700; letter-spacing:1px; margin-bottom:10px; text-transform:uppercase;
}

.metric-card {
    background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1);
    border-radius:16px; padding:22px; text-align:center;
}
.metric-card .val { font-size:2.2rem; font-weight:900; color:#667eea; }
.metric-card .lbl { color:rgba(255,255,255,.6); font-size:.85rem; margin-top:4px; }

.code-block {
    background:#1e1e2e; border:1px solid #333355; border-radius:12px;
    padding:18px; font-family:'Fira Code',monospace; font-size:.82rem;
    color:#cdd6f4; overflow-x:auto; line-height:1.7;
}

.insight-box {
    background:linear-gradient(135deg,rgba(102,126,234,.15),rgba(118,75,162,.15));
    border:1px solid rgba(102,126,234,.4); border-radius:14px; padding:18px 22px;
}
.insight-box strong { color:#a78bfa; }

.compare-header {
    background:rgba(255,255,255,.04); border-radius:12px; padding:12px 20px;
    text-align:center; font-weight:700; color:#e2e8f0; margin-bottom:14px;
    border:1px solid rgba(255,255,255,.08);
}
.mpl-header { border-top:3px solid #ef4444 !important; }
.sns-header { border-top:3px solid #22c55e !important; }

.advantage-pill {
    display:inline-block; background:rgba(34,197,94,.15); border:1px solid rgba(34,197,94,.4);
    color:#4ade80; border-radius:20px; padding:3px 12px; font-size:.78rem;
    margin:3px; font-weight:600;
}
.warning-pill {
    display:inline-block; background:rgba(239,68,68,.15); border:1px solid rgba(239,68,68,.4);
    color:#f87171; border-radius:20px; padding:3px 12px; font-size:.78rem; margin:3px;
}

div[data-baseweb="tab-list"] { background:rgba(255,255,255,.04) !important; border-radius:12px; padding:4px; }
div[data-baseweb="tab"] { color:rgba(255,255,255,.6) !important; border-radius:8px !important; font-weight:600; }
div[data-baseweb="tab"][aria-selected="true"] {
    background:linear-gradient(90deg,#667eea,#764ba2) !important; color:#fff !important;
}

.stSelectbox label, .stRadio label, .stSlider label { color:rgba(255,255,255,.7) !important; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ─── Veri Seti ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 200
    tips = sns.load_dataset("tips")
    iris = sns.load_dataset("iris")
    penguins = sns.load_dataset("penguins").dropna()
    return tips, iris, penguins

tips, iris, penguins = load_data()

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Ders Menüsü")
    st.markdown("---")
    section = st.radio(
        "Bölüm Seç",
        ["🏠 Giriş & Genel Bakış",
         "📈 Grafik Türleri Karşılaştırması",
         "🎨 Stil & Estetik",
         "📊 İstatistiksel Grafikler",
         "🔗 İlişki Grafikleri",
         "🧩 Çoklu Grafik (FacetGrid)",
         "🏆 Seaborn'un Süper Güçleri",
         "🧪 Canlı Deney Alanı"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("""
    <div style='background:rgba(102,126,234,.15);border-radius:10px;padding:14px;'>
    <p style='color:#a78bfa;font-weight:700;margin:0 0 6px;'>💡 Hızlı Bilgi</p>
    <p style='color:rgba(255,255,255,.7);font-size:.82rem;margin:0;'>
    Seaborn, Matplotlib üzerine inşa edilmiştir. Seaborn = Matplotlib + istatistik + güzel varsayılanlar
    </p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 0 — GİRİŞ
# ════════════════════════════════════════════════════════════════════════════
if section == "🏠 Giriş & Genel Bakış":
    st.markdown("""
    <div class='hero-card'>
      <h1>📊 Matplotlib vs Seaborn</h1>
      <p>Python'da Veri Görselleştirme — Karşılaştırmalı Öğrenme Platformu</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [("7", "Karşılaştırma Bölümü"), ("15+", "Örnek Grafik"), ("3", "Gerçek Veri Seti"), ("∞", "Deney Alanı")]
    for col, (val, lbl) in zip([c1,c2,c3,c4], metrics):
        col.markdown(f"<div class='metric-card'><div class='val'>{val}</div><div class='lbl'>{lbl}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("### 🐍 Matplotlib Nedir?")
        st.markdown("""
        <div class='insight-box'>
        <p style='color:rgba(255,255,255,.85);'>
        <strong>Matplotlib</strong>, 2003 yılında John Hunter tarafından geliştirilen Python'ın temel görselleştirme kütüphanesidir.
        </p>
        <ul style='color:rgba(255,255,255,.75);'>
        <li>Tam kontrol ve esneklik</li>
        <li>Düşük seviye API</li>
        <li>Her şeyi manuel olarak ayarlama</li>
        <li>Akademik yayınlar için uygundur</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown("### 🌊 Seaborn Nedir?")
        st.markdown("""
        <div class='insight-box'>
        <p style='color:rgba(255,255,255,.85);'>
        <strong>Seaborn</strong>, Matplotlib tabanlı, istatistiksel veri görselleştirmeye odaklanan yüksek seviyeli bir kütüphanedir.
        </p>
        <ul style='color:rgba(255,255,255,.75);'>
        <li>Varsayılan güzel temalar</li>
        <li>İstatistiksel fonksiyonlar dahili</li>
        <li>Pandas DataFrame ile mükemmel uyum</li>
        <li>Az kod → çok anlam</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚖️ Temel Farklar — Hızlı Özet")
    comparison_data = {
        "Özellik": ["Kuruluş Yılı", "Kod Uzunluğu", "Varsayılan Stil", "İstatistik Desteği",
                    "DataFrame Uyumu", "Öğrenme Eğrisi", "Esneklik", "İdeal Kullanım"],
        "Matplotlib": ["2003", "Uzun / Detaylı", "Sade / Ham", "❌ Yok",
                       "Orta", "Dik", "⭐⭐⭐⭐⭐", "Tam kontrol gereken grafikler"],
        "Seaborn": ["2012", "Kısa / Öz", "Modern / Şık", "✅ Dahili",
                    "Mükemmel", "Hafif", "⭐⭐⭐", "İstatistiksel keşifler"],
    }
    df_comp = pd.DataFrame(comparison_data)
    st.dataframe(df_comp.set_index("Özellik"), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 1 — GRAFİK TÜRLERİ KARŞILAŞTIRMASI
# ════════════════════════════════════════════════════════════════════════════
elif section == "📈 Grafik Türleri Karşılaştırması":
    st.markdown("<div class='section-badge'>Bölüm 1</div>", unsafe_allow_html=True)
    st.markdown("## 📈 Aynı Grafik — İki Farklı Kütüphane")

    chart_type = st.selectbox(
        "Grafik Türünü Seçin",
        ["Histogram", "Saçılım Grafiği (Scatter)", "Çubuk Grafik (Bar)", "Kutu Grafiği (Box)"]
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor="#0f0f1a")
    for ax in [ax1, ax2]:
        ax.set_facecolor("#1a1a2e")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

    if chart_type == "Histogram":
        col_mpl, col_sns = st.columns(2)

        # Matplotlib
        ax1.hist(tips["total_bill"], bins=25, color="#ef4444", edgecolor="white", alpha=0.8)
        ax1.set_title("Matplotlib — Histogram", color="white", fontsize=13, fontweight="bold", pad=12)
        ax1.set_xlabel("Hesap Tutarı ($)", color="#aaa"); ax1.set_ylabel("Frekans", color="#aaa")
        ax1.tick_params(colors="#aaa")

        # Seaborn
        sns.histplot(tips["total_bill"], bins=25, kde=True, ax=ax2, color="#667eea",
                     edgecolor="white", alpha=0.8)
        ax2.set_title("Seaborn — histplot (KDE dahil!)", color="white", fontsize=13, fontweight="bold", pad=12)
        ax2.set_xlabel("Hesap Tutarı ($)", color="#aaa"); ax2.set_ylabel("", color="#aaa")
        ax2.tick_params(colors="#aaa"); ax2.set_facecolor("#1a1a2e")

        code_mpl = """# Matplotlib — 8 satır
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.hist(tips['total_bill'], bins=25,
        color='red', edgecolor='white')
ax.set_xlabel('Hesap ($)')
ax.set_ylabel('Frekans')
plt.show()"""

        code_sns = """# Seaborn — 3 satır (KDE ile birlikte!)
import seaborn as sns
sns.histplot(tips['total_bill'],
             bins=25, kde=True)
plt.show()"""

        with col_mpl:
            st.markdown("<div class='compare-header mpl-header'>🔴 Matplotlib</div>", unsafe_allow_html=True)
            st.code(code_mpl, language="python")
            st.markdown("<span class='warning-pill'>8 satır kod</span> <span class='warning-pill'>KDE yok</span>", unsafe_allow_html=True)

        with col_sns:
            st.markdown("<div class='compare-header sns-header'>🟢 Seaborn</div>", unsafe_allow_html=True)
            st.code(code_sns, language="python")
            st.markdown("<span class='advantage-pill'>3 satır kod</span> <span class='advantage-pill'>KDE dahil</span>", unsafe_allow_html=True)

    elif chart_type == "Saçılım Grafiği (Scatter)":
        col_mpl, col_sns = st.columns(2)
        colors_mpl = {"Lunch": "#ef4444", "Dinner": "#3b82f6"}
        for time_val, grp in tips.groupby("time"):
            ax1.scatter(grp["total_bill"], grp["tip"], label=time_val,
                        color=colors_mpl[time_val], alpha=0.7, edgecolors="white", lw=0.5)
        ax1.set_title("Matplotlib — Scatter", color="white", fontsize=13, fontweight="bold", pad=12)
        ax1.set_xlabel("Hesap ($)", color="#aaa"); ax1.set_ylabel("Bahşiş ($)", color="#aaa")
        ax1.tick_params(colors="#aaa"); ax1.legend(facecolor="#1a1a2e", labelcolor="white")

        sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time",
                        style="sex", size="size", ax=ax2, palette="viridis", alpha=0.8)
        ax2.set_title("Seaborn — scatterplot (hue+style+size!)", color="white", fontsize=13, fontweight="bold", pad=12)
        ax2.set_xlabel("Hesap ($)", color="#aaa"); ax2.set_ylabel("", color="#aaa")
        ax2.tick_params(colors="#aaa"); ax2.set_facecolor("#1a1a2e")
        ax2.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=8)

        with col_mpl:
            st.markdown("<div class='compare-header mpl-header'>🔴 Matplotlib</div>", unsafe_allow_html=True)
            st.code("""# Matplotlib — Elle renk yönetimi
colors = {'Lunch':'red','Dinner':'blue'}
for time, grp in tips.groupby('time'):
    ax.scatter(grp['total_bill'], grp['tip'],
               label=time, color=colors[time])
ax.legend()""", language="python")
            st.markdown("<span class='warning-pill'>Manuel gruplandırma</span> <span class='warning-pill'>Tek boyut</span>", unsafe_allow_html=True)

        with col_sns:
            st.markdown("<div class='compare-header sns-header'>🟢 Seaborn</div>", unsafe_allow_html=True)
            st.code("""# Seaborn — 1 satırda 4 boyut!
sns.scatterplot(data=tips,
    x='total_bill', y='tip',
    hue='time', style='sex',
    size='size')""", language="python")
            st.markdown("<span class='advantage-pill'>hue</span> <span class='advantage-pill'>style</span> <span class='advantage-pill'>size</span> <span class='advantage-pill'>Otomatik legend</span>", unsafe_allow_html=True)

    elif chart_type == "Çubuk Grafik (Bar)":
        col_mpl, col_sns = st.columns(2)
        days = tips["day"].unique()
        means = [tips[tips["day"]==d]["total_bill"].mean() for d in days]
        stds  = [tips[tips["day"]==d]["total_bill"].std()  for d in days]
        bars = ax1.bar(days, means, yerr=stds, color="#ef4444", alpha=0.8,
                       edgecolor="white", capsize=5, error_kw={"ecolor":"white"})
        ax1.set_title("Matplotlib — Bar (Manuel CI)", color="white", fontsize=13, fontweight="bold", pad=12)
        ax1.set_xlabel("Gün", color="#aaa"); ax1.set_ylabel("Ort. Hesap ($)", color="#aaa")
        ax1.tick_params(colors="#aaa")

        sns.barplot(data=tips, x="day", y="total_bill", hue="sex",
                    palette="coolwarm", ax=ax2, capsize=0.1, errorbar="sd")
        ax2.set_title("Seaborn — barplot (CI otomatik + hue!)", color="white", fontsize=13, fontweight="bold", pad=12)
        ax2.set_xlabel("Gün", color="#aaa"); ax2.set_ylabel("", color="#aaa")
        ax2.tick_params(colors="#aaa"); ax2.set_facecolor("#1a1a2e")
        ax2.legend(facecolor="#1a1a2e", labelcolor="white")

        with col_mpl:
            st.markdown("<div class='compare-header mpl-header'>🔴 Matplotlib</div>", unsafe_allow_html=True)
            st.code("""# Manuel hesaplama
means = tips.groupby('day')['total_bill'].mean()
stds  = tips.groupby('day')['total_bill'].std()
ax.bar(days, means, yerr=stds, capsize=5)""", language="python")
            st.markdown("<span class='warning-pill'>Manuel CI hesabı</span> <span class='warning-pill'>Gruplama yok</span>", unsafe_allow_html=True)

        with col_sns:
            st.markdown("<div class='compare-header sns-header'>🟢 Seaborn</div>", unsafe_allow_html=True)
            st.code("""# Seaborn — her şey otomatik
sns.barplot(data=tips,
    x='day', y='total_bill',
    hue='sex', errorbar='sd')""", language="python")
            st.markdown("<span class='advantage-pill'>CI otomatik</span> <span class='advantage-pill'>Gruplama dahil</span>", unsafe_allow_html=True)

    else:  # Box
        col_mpl, col_sns = st.columns(2)
        day_order = ["Thur","Fri","Sat","Sun"]
        data_by_day = [tips[tips["day"]==d]["total_bill"].values for d in day_order]
        bp = ax1.boxplot(data_by_day, labels=day_order, patch_artist=True,
                         boxprops=dict(facecolor="#ef4444", alpha=0.7),
                         medianprops=dict(color="white", linewidth=2),
                         whiskerprops=dict(color="#aaa"), capprops=dict(color="#aaa"),
                         flierprops=dict(markerfacecolor="#aaa", marker="o", markersize=4))
        ax1.set_title("Matplotlib — Boxplot (Manuel)", color="white", fontsize=13, fontweight="bold", pad=12)
        ax1.set_xlabel("Gün", color="#aaa"); ax1.set_ylabel("Hesap ($)", color="#aaa")
        ax1.tick_params(colors="#aaa")

        sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker",
                    palette="Set2", ax=ax2, order=day_order)
        sns.stripplot(data=tips, x="day", y="total_bill", ax=ax2, order=day_order,
                      color="white", alpha=0.3, size=3, jitter=True)
        ax2.set_title("Seaborn — boxplot + stripplot!", color="white", fontsize=13, fontweight="bold", pad=12)
        ax2.set_xlabel("Gün", color="#aaa"); ax2.set_ylabel("", color="#aaa")
        ax2.tick_params(colors="#aaa"); ax2.set_facecolor("#1a1a2e")
        ax2.legend(facecolor="#1a1a2e", labelcolor="white")

        with col_mpl:
            st.markdown("<div class='compare-header mpl-header'>🔴 Matplotlib</div>", unsafe_allow_html=True)
            st.code("""# Matplotlib — veriyi liste olarak hazırla
data = [tips[tips['day']==d]['total_bill']
        for d in ['Thur','Fri','Sat','Sun']]
ax.boxplot(data, patch_artist=True)""", language="python")
            st.markdown("<span class='warning-pill'>Manuel veri hazırlama</span>", unsafe_allow_html=True)

        with col_sns:
            st.markdown("<div class='compare-header sns-header'>🟢 Seaborn</div>", unsafe_allow_html=True)
            st.code("""# Seaborn — DataFrame direkt kullan
sns.boxplot(data=tips, x='day',
            y='total_bill', hue='smoker')
sns.stripplot(data=tips, x='day',
              y='total_bill', alpha=0.3)""", language="python")
            st.markdown("<span class='advantage-pill'>DataFrame direkt</span> <span class='advantage-pill'>Katman bindirme</span>", unsafe_allow_html=True)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 2 — STİL & ESTETİK
# ════════════════════════════════════════════════════════════════════════════
elif section == "🎨 Stil & Estetik":
    st.markdown("<div class='section-badge'>Bölüm 2</div>", unsafe_allow_html=True)
    st.markdown("## 🎨 Seaborn Temaları ve Renk Paletleri")

    c1, c2 = st.columns(2)
    with c1:
        theme = st.selectbox("Seaborn Teması", ["darkgrid","whitegrid","dark","white","ticks"])
    with c2:
        palette = st.selectbox("Renk Paleti", ["deep","muted","bright","pastel","dark","colorblind","viridis","magma","coolwarm","Set2"])

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor="#0f0f1a")

    with sns.axes_style(theme):
        sns.set_palette(palette)

        # Panel 1: violinplot
        df_v = penguins.copy()
        sns.violinplot(data=df_v, x="species", y="body_mass_g", hue="sex",
                       split=True, inner="quart", ax=axes[0], palette=palette)
        axes[0].set_title(f"Violin Plot\nTema: {theme}", fontweight="bold", pad=10)
        axes[0].set_xlabel("Tür"); axes[0].set_ylabel("Vücut Kütlesi (g)")

        # Panel 2: stripplot + boxplot
        sns.boxplot(data=penguins, x="species", y="flipper_length_mm",
                    ax=axes[1], palette=palette, width=0.4)
        sns.stripplot(data=penguins, x="species", y="flipper_length_mm",
                      ax=axes[1], color=".3", size=3, jitter=True, alpha=0.5)
        axes[1].set_title("Box + Strip (Katmanlı)", fontweight="bold", pad=10)
        axes[1].set_xlabel("Tür"); axes[1].set_ylabel("Kanat Uzunluğu (mm)")

        # Panel 3: kdeplot
        for sp in penguins["species"].unique():
            sub = penguins[penguins["species"]==sp]
            sns.kdeplot(data=sub, x="bill_length_mm", y="bill_depth_mm",
                        ax=axes[2], fill=True, alpha=0.4, label=sp)
        axes[2].set_title("2D KDE Plot", fontweight="bold", pad=10)
        axes[2].set_xlabel("Gaga Uzunluğu (mm)"); axes[2].set_ylabel("Gaga Derinliği (mm)")
        axes[2].legend(fontsize=8)

    for ax in axes:
        ax.set_facecolor("#1a1a2e")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")
        ax.title.set_color("white"); ax.xaxis.label.set_color("#aaa")
        ax.yaxis.label.set_color("#aaa"); ax.tick_params(colors="#aaa")
        leg = ax.get_legend()
        if leg:
            leg.get_frame().set_facecolor("#1a1a2e")
            for t in leg.get_texts(): t.set_color("white")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.markdown("### 💡 Seaborn'da Tema Değiştirmek — Sadece 2 Satır!")
    st.code(f"""import seaborn as sns
sns.set_theme(style='{theme}', palette='{palette}')
# ve grafikleriniz otomatik olarak bu temayı kullanır!""", language="python")

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 3 — İSTATİSTİKSEL GRAFİKLER
# ════════════════════════════════════════════════════════════════════════════
elif section == "📊 İstatistiksel Grafikler":
    st.markdown("<div class='section-badge'>Bölüm 3</div>", unsafe_allow_html=True)
    st.markdown("## 📊 Seaborn'un İstatistiksel Süper Güçleri")
    st.markdown("""
    <div class='insight-box'>
    <strong>Neden önemli?</strong> Seaborn, tek bir fonksiyonla güven aralıkları, regresyon çizgileri
    ve dağılım tahminleri gibi istatistiksel katmanlar ekler. Matplotlib'de bunlar için ayrı hesaplamalar gerekir.
    </div>
    """, unsafe_allow_html=True)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10), facecolor="#0f0f1a")
    axes = axes.flatten()
    for ax in axes:
        ax.set_facecolor("#1a1a2e")
        for spine in ax.spines.values(): spine.set_edgecolor("#333355")
        ax.tick_params(colors="#aaa")

    # 1. regplot
    sns.regplot(data=tips, x="total_bill", y="tip", ax=axes[0],
                scatter_kws={"alpha":0.6,"color":"#667eea","edgecolors":"white","linewidths":0.5},
                line_kws={"color":"#f59e0b","linewidth":2.5},
                ci=95)
    axes[0].set_title("regplot — Regresyon + %95 CI", color="white", fontweight="bold")
    axes[0].set_xlabel("Hesap ($)", color="#aaa"); axes[0].set_ylabel("Bahşiş ($)", color="#aaa")

    # 2. residplot
    sns.residplot(data=tips, x="total_bill", y="tip", ax=axes[1],
                  scatter_kws={"alpha":0.6,"color":"#f59e0b","edgecolors":"white","linewidths":0.5},
                  line_kws={"color":"#ef4444","linewidth":2})
    axes[1].set_title("residplot — Artık Analizi", color="white", fontweight="bold")
    axes[1].set_xlabel("Hesap ($)", color="#aaa"); axes[1].set_ylabel("Artık (Residual)", color="#aaa")

    # 3. kdeplot
    sns.kdeplot(data=tips, x="total_bill", hue="time", fill=True, alpha=0.5,
                ax=axes[2], palette={"Lunch":"#667eea","Dinner":"#f59e0b"})
    axes[2].set_title("kdeplot — Çekirdek Yoğunluk", color="white", fontweight="bold")
    axes[2].set_xlabel("Hesap ($)", color="#aaa"); axes[2].set_ylabel("Yoğunluk", color="#aaa")
    leg = axes[2].get_legend()
    if leg:
        leg.get_frame().set_facecolor("#1a1a2e")
        for t in leg.get_texts(): t.set_color("white")

    # 4. ecdfplot
    sns.ecdfplot(data=tips, x="total_bill", hue="day", ax=axes[3],
                 palette="Set2", linewidth=2)
    axes[3].set_title("ecdfplot — Kümülatif Dağılım", color="white", fontweight="bold")
    axes[3].set_xlabel("Hesap ($)", color="#aaa"); axes[3].set_ylabel("Kümülatif Oran", color="#aaa")
    leg = axes[3].get_legend()
    if leg:
        leg.get_frame().set_facecolor("#1a1a2e")
        for t in leg.get_texts(): t.set_color("white")

    # 5. violinplot
    sns.violinplot(data=penguins, x="species", y="body_mass_g", hue="sex",
                   split=True, inner="quartile", ax=axes[4], palette="coolwarm")
    axes[4].set_title("violinplot — Dağılım + KDE", color="white", fontweight="bold")
    axes[4].set_xlabel("Tür", color="#aaa"); axes[4].set_ylabel("Kütle (g)", color="#aaa")
    leg = axes[4].get_legend()
    if leg:
        leg.get_frame().set_facecolor("#1a1a2e")
        for t in leg.get_texts(): t.set_color("white")

    # 6. heatmap
    corr = tips[["total_bill","tip","size"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=axes[5],
                linewidths=0.5, linecolor="#333355",
                annot_kws={"color":"white","size":12},
                cbar_kws={"shrink":0.8})
    axes[5].set_title("heatmap — Korelasyon Matrisi", color="white", fontweight="bold")
    axes[5].tick_params(colors="#aaa")

    plt.suptitle("Seaborn İstatistiksel Grafik Galerisi", color="white",
                 fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 4 — İLİŞKİ GRAFİKLERİ
# ════════════════════════════════════════════════════════════════════════════
elif section == "🔗 İlişki Grafikleri":
    st.markdown("<div class='section-badge'>Bölüm 4</div>", unsafe_allow_html=True)
    st.markdown("## 🔗 İlişki Grafikleri — pairplot & heatmap")

    tab1, tab2 = st.tabs(["🔵 Pair Plot", "🟠 Correlation Heatmap"])

    with tab1:
        st.markdown("### pairplot — Tüm Değişken Çiftleri Tek Komutta!")
        col1, col2  = st.columns([1,3])
        with col1:
            dataset_choice = st.radio("Veri Seti", ["Penguins", "Iris", "Tips"])
            diag_kind = st.radio("Köşegen Tür", ["kde","hist","auto"])
            hue_col = st.radio("Renk (hue)", ["species"] if dataset_choice in ["Penguins","Iris"] else ["sex","day","smoker"])

        with col2:
            if dataset_choice == "Penguins":
                df_pp = penguins
            elif dataset_choice == "Iris":
                df_pp = iris
                hue_col = "species"
            else:
                df_pp = tips
                hue_col = "sex"

            with st.spinner("Grafik oluşturuluyor..."):
                g = sns.pairplot(df_pp, hue=hue_col, diag_kind=diag_kind,
                                 palette="viridis", plot_kws={"alpha":0.6,"edgecolors":"white","linewidths":0.3})
                g.figure.set_facecolor("#1a1a2e")
                for ax in g.axes.flatten():
                    if ax:
                        ax.set_facecolor("#0f0f1a")
                        for sp in ax.spines.values(): sp.set_edgecolor("#333355")
                        ax.tick_params(colors="#aaa", labelsize=7)
                        ax.xaxis.label.set_color("#aaa")
                        ax.yaxis.label.set_color("#aaa")
                st.pyplot(g.figure)
                plt.close()

        st.code(f"""# Tüm bu grafikleri üretmek için sadece 1 satır!
sns.pairplot(df, hue='{hue_col}', diag_kind='{diag_kind}', palette='viridis')""", language="python")

    with tab2:
        st.markdown("### Korelasyon Isı Haritası (Heatmap)")
        num_cols = penguins.select_dtypes(include=np.number).columns.tolist()
        corr_method = st.radio("Korelasyon Yöntemi", ["pearson","spearman","kendall"], horizontal=True)
        corr_matrix = penguins[num_cols].corr(method=corr_method)

        fig, ax = plt.subplots(figsize=(9, 7), facecolor="#0f0f1a")
        ax.set_facecolor("#1a1a2e")
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
                    ax=ax, linewidths=1, linecolor="#0f0f1a", center=0,
                    annot_kws={"size":11,"color":"#1a1a2e","weight":"bold"},
                    vmin=-1, vmax=1)
        ax.set_title(f"Penguen Veri Seti — {corr_method.title()} Korelasyonu",
                     color="white", fontsize=13, fontweight="bold", pad=15)
        ax.tick_params(colors="#aaa")
        st.pyplot(fig); plt.close()

        st.code(f"""import seaborn as sns, numpy as np
corr = df.corr(method='{corr_method}')
mask = np.triu(np.ones_like(corr, dtype=bool))  # üst üçgeni gizle
sns.heatmap(corr, mask=mask, annot=True,
            fmt='.2f', cmap='RdYlGn', center=0)""", language="python")

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 5 — FACETGRID
# ════════════════════════════════════════════════════════════════════════════
elif section == "🧩 Çoklu Grafik (FacetGrid)":
    st.markdown("<div class='section-badge'>Bölüm 5</div>", unsafe_allow_html=True)
    st.markdown("## 🧩 FacetGrid — Alt Grafikleri Otomatik Oluşturma")
    st.markdown("""
    <div class='insight-box'>
    <strong>FacetGrid</strong>, veriyi kategorik bir değişkene göre bölerek her alt grup için aynı grafiği otomatik çizer.
    Matplotlib'de bunu yapmak onlarca satır döngü kodu gerektirir!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        facet_col = st.selectbox("Sütun (col)", ["time","smoker"])
        facet_row = st.selectbox("Satır (row)", ["sex", "Yok"])
        plot_kind  = st.selectbox("Grafik Türü", ["histplot","scatterplot","kdeplot"])

    with col2:
        with st.spinner("FacetGrid oluşturuluyor..."):
            row_var = "sex" if facet_row != "Yok" else None
            g = sns.FacetGrid(tips, col=facet_col, row=row_var,
                              height=4, aspect=1.4, palette="coolwarm")
            if plot_kind == "histplot":
                g.map_dataframe(sns.histplot, x="total_bill", kde=True, color="#667eea")
            elif plot_kind == "scatterplot":
                g.map_dataframe(sns.scatterplot, x="total_bill", y="tip",
                                alpha=0.7, color="#f59e0b")
            else:
                g.map_dataframe(sns.kdeplot, x="total_bill", fill=True,
                                alpha=0.6, color="#22c55e")
            g.add_legend()
            g.figure.set_facecolor("#0f0f1a")
            for ax in g.axes.flatten():
                ax.set_facecolor("#1a1a2e")
                for sp in ax.spines.values(): sp.set_edgecolor("#333355")
                ax.tick_params(colors="#aaa")
                ax.set_xlabel("Hesap ($)", color="#aaa"); ax.set_ylabel("", color="#aaa")
                ax.title.set_color("white")
            st.pyplot(g.figure); plt.close()

    st.markdown("---")
    row_str = f", row='{facet_row}'" if facet_row != "Yok" else ""
    st.code(f"""# FacetGrid — karmaşık alt grafikleri 3 satırda!
g = sns.FacetGrid(tips, col='{facet_col}'{row_str}, height=4)
g.map_dataframe(sns.{plot_kind}, x='total_bill')
g.add_legend()""", language="python")

    st.markdown("### Matplotlib ile Eşdeğer Kod (Karşılaştırma)")
    st.code("""# Matplotlib — aynı iş için ~20 satır
fig, axes = plt.subplots(2, 2, figsize=(12,8))
for i, (sex, sex_grp) in enumerate(tips.groupby('sex')):
    for j, (time, time_grp) in enumerate(sex_grp.groupby('time')):
        ax = axes[i][j]
        ax.hist(time_grp['total_bill'], bins=20)
        ax.set_title(f'{sex} | {time}')
        ax.set_xlabel('Hesap ($)')
plt.tight_layout()
plt.show()""", language="python")

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 6 — SÜPER GÜÇLER
# ════════════════════════════════════════════════════════════════════════════
elif section == "🏆 Seaborn'un Süper Güçleri":
    st.markdown("<div class='section-badge'>Bölüm 6</div>", unsafe_allow_html=True)
    st.markdown("## 🏆 Seaborn'un Süper Güçleri")

    powers = [
        ("🎯 Dahili İstatistik", "Güven aralıkları, KDE, regresyon otomatik hesaplanır", "advantage"),
        ("🐼 Pandas Uyumu",     "DataFrame'i doğrudan kullanın, dönüşüm gerekmez",     "advantage"),
        ("🎨 Güzel Varsayılanlar","Hiç kod yazmadan şık grafikler",                     "advantage"),
        ("📐 FacetGrid",        "Alt grafikleri 3 satırda oluşturun",                   "advantage"),
        ("🔀 hue / size / style","Tek grafikte 4+ boyutu görselleştirin",               "advantage"),
        ("⚡ Az Kod",           "Matplotlib'den 3–5× daha az satır",                    "advantage"),
    ]

    cols = st.columns(3)
    for i, (icon_title, desc, ptype) in enumerate(powers):
        color = "#22c55e" if ptype=="advantage" else "#ef4444"
        cols[i%3].markdown(f"""
        <div style='background:rgba(255,255,255,.04);border:1px solid {color}44;
        border-radius:14px;padding:20px;margin-bottom:16px;border-top:3px solid {color};'>
        <p style='font-size:1.1rem;font-weight:700;color:white;margin:0 0 8px;'>{icon_title}</p>
        <p style='color:rgba(255,255,255,.65);font-size:.88rem;margin:0;'>{desc}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📏 Kod Uzunluğu Karşılaştırması")

    comparisons = [
        ("Histogram + KDE",     8, 3),
        ("Scatter + Hue",       15, 4),
        ("Bar + CI",            12, 3),
        ("Pair Plot",           40, 1),
        ("Heatmap",             20, 5),
        ("FacetGrid",           25, 3),
    ]
    df_lines = pd.DataFrame(comparisons, columns=["Grafik Türü","Matplotlib Satırı","Seaborn Satırı"])

    fig, ax = plt.subplots(figsize=(12, 5), facecolor="#0f0f1a")
    ax.set_facecolor("#1a1a2e")
    x = np.arange(len(df_lines))
    w = 0.35
    bars1 = ax.bar(x - w/2, df_lines["Matplotlib Satırı"], w, label="Matplotlib",
                   color="#ef4444", alpha=0.85, edgecolor="white", linewidth=0.5)
    bars2 = ax.bar(x + w/2, df_lines["Seaborn Satırı"],   w, label="Seaborn",
                   color="#22c55e", alpha=0.85, edgecolor="white", linewidth=0.5)
    ax.bar_label(bars1, fmt="%d", color="white", fontsize=10, fontweight="bold")
    ax.bar_label(bars2, fmt="%d", color="white", fontsize=10, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(df_lines["Grafik Türü"], color="#aaa", rotation=15, ha="right")
    ax.set_ylabel("Ortalama Kod Satırı Sayısı", color="#aaa")
    ax.set_title("Aynı Grafiği Üretmek İçin Gereken Satır Sayısı", color="white", fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors="#aaa"); ax.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=11)
    for spine in ax.spines.values(): spine.set_edgecolor("#333355")
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════════════════════
# BÖLÜM 7 — CANLI DENEY ALANI
# ════════════════════════════════════════════════════════════════════════════
elif section == "🧪 Canlı Deney Alanı":
    st.markdown("<div class='section-badge'>Bölüm 7</div>", unsafe_allow_html=True)
    st.markdown("## 🧪 Canlı Deney Alanı — Parametreleri Değiştir, Sonucu Gör!")

    c1, c2, c3 = st.columns(3)
    with c1:
        ds   = st.selectbox("Veri Seti", ["Tips","Penguins","Iris"])
        gtype= st.selectbox("Grafik", ["violinplot","boxplot","swarmplot","stripplot","barplot","pointplot"])
    with c2:
        palette_live = st.selectbox("Renk Paleti", ["deep","muted","Set2","coolwarm","viridis","magma","Spectral"])
        style_live   = st.selectbox("Tema", ["darkgrid","whitegrid","dark","ticks"])
    with c3:
        inner_v = st.select_slider("Violin İç Gösterim", ["box","quart","point","stick","None"])
        alpha_v = st.slider("Şeffaflık (alpha)", 0.1, 1.0, 0.8, 0.05)

    if ds == "Tips":
        df_live, x_col, y_col, hue_col = tips, "day", "total_bill", "sex"
    elif ds == "Penguins":
        df_live, x_col, y_col, hue_col = penguins, "species", "body_mass_g", "sex"
    else:
        df_live, x_col, y_col, hue_col = iris, "species", "sepal_length", None

    sns.set_theme(style=style_live, palette=palette_live)
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="#0f0f1a")
    ax.set_facecolor("#1a1a2e")
    for spine in ax.spines.values(): spine.set_edgecolor("#333355")

    try:
        kwargs = dict(data=df_live, x=x_col, y=y_col, ax=ax, palette=palette_live)
        if hue_col: kwargs["hue"] = hue_col

        if gtype == "violinplot":
            inner_val = None if inner_v == "None" else inner_v
            sns.violinplot(**kwargs, inner=inner_val, alpha=alpha_v)
        elif gtype == "boxplot":
            sns.boxplot(**kwargs)
        elif gtype == "swarmplot":
            sns.swarmplot(**kwargs, size=4, alpha=alpha_v)
        elif gtype == "stripplot":
            sns.stripplot(**kwargs, jitter=True, size=5, alpha=alpha_v)
        elif gtype == "barplot":
            sns.barplot(**kwargs, errorbar="sd", capsize=0.1)
        elif gtype == "pointplot":
            sns.pointplot(**kwargs, errorbar="sd", capsize=0.2,
                          markers="o", linestyles="--")

        ax.set_title(f"sns.{gtype}  |  Veri: {ds}  |  Tema: {style_live}",
                     color="white", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel(x_col, color="#aaa"); ax.set_ylabel(y_col, color="#aaa")
        ax.tick_params(colors="#aaa")
        leg = ax.get_legend()
        if leg:
            leg.get_frame().set_facecolor("#1a1a2e")
            for t in leg.get_texts(): t.set_color("white")

    except Exception as e:
        ax.text(0.5, 0.5, f"Hata: {e}", transform=ax.transAxes,
                ha="center", va="center", color="#ef4444", fontsize=11)

    st.pyplot(fig); plt.close()

    hue_str = f", hue='{hue_col}'" if hue_col else ""
    st.code(f"""sns.set_theme(style='{style_live}', palette='{palette_live}')
sns.{gtype}(data=df, x='{x_col}', y='{y_col}'{hue_str})
plt.show()""", language="python")

    sns.set_theme()  # varsayılana sıfırla

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:rgba(255,255,255,.35);font-size:.8rem;padding:12px 0;'>
📊 Matplotlib vs Seaborn | Veri Görselleştirme Eğitim Platformu &nbsp;·&nbsp;
Gerçek veri setleri: <em>tips, penguins, iris</em> (Seaborn dahili)
</div>
""", unsafe_allow_html=True)
