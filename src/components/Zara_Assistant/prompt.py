import re

table_list = [
    'table', 'summary', 'summarize', 'rangkum', 'rangkuman', 'tabel', 'daftar', 'rekap', 'rekapan',
    'data', 'list', 'rincian', 'ringkasan', 'resume', 'overview', 'display table', 'tabulasi',
    'lihat tabel', 'tampilkan tabel', 'show table', 'lihat data', 'generate table', 'create table',
    'buat tabel', 'export table', 'data tabular', 'table format', 'tabel ringkasan',
    'detail tabel', 'dataframe', 'df', 'row', 'kolom', 'kolom-kolom', 'baris', 'baris-baris',
    'table report', 'rekap data', 'tabel hasil', 'result table', 'output table', 'matrix',
    'tabel analisis', 'tabel informasi', 'tabular', 'info tabel'
]

plot_list = [
    'plot', 'graph', 'chart', 'diagram', 'visualisasi', 'visualisasi data', 'grafik', 'graf',
    'line chart', 'bar chart', 'pie chart', 'scatter plot', 'histogram', 'box plot',
    'donut chart', 'area chart', 'heatmap', 'timeseries', 'trend', 'kurva', 'plotkan',
    'buat grafik', 'tampilkan grafik', 'show chart', 'generate plot', 'visualisasi grafik',
    'visualisasi chart', 'buat diagram', 'grafik batang', 'grafik garis', 'grafik lingkaran',
    'grafik sebar', 'grafik area', 'grafik tren', 'plot data', 'visual chart', 'plot hasil',
    'data visual', 'render chart', 'grafik performa', 'visual report', 'output chart',
    'plot summary', 'gambar grafik', 'grafik output', 'plot visualisasi'
]

def detect_intent(user_input: str):
    user_input_lower = user_input.lower()
    for keyword in plot_list:
        if re.search(rf'\b{re.escape(keyword)}\b', user_input_lower):
            return "plot"
    for keyword in table_list:
        if re.search(rf'\b{re.escape(keyword)}\b', user_input_lower):
            return "table"
    return "unknown"

def generate_prompt(df, question, metadata_desc=None, table_name="Unknown Table"):
    # Basic DataFrame Summary (token-efficient)
    df_preview = df.head(5).to_string(index=False)
    summary_stats = df.describe(include='all').transpose()
    column_info = [f"- '{col}': {df[col].nunique()} unique, {df[col].isnull().sum()} missing" for col in df.columns]

    # Categorical Mode
    common_values = []
    for col in df.select_dtypes(include='object').columns:
        if not df[col].empty:
            common_values.append(f"- Most common in '{col}': {df[col].mode().iloc[0]}")
    
    unique_values_summary = []
    for col in df.select_dtypes(include=['object', 'category']).columns:
        uniques = df[col].dropna().unique()
        truncated = [str(u)[:30] for u in uniques[:10]]  # limit length and number
        unique_values_summary.append(f"- '{col}': {truncated}" + ("..." if len(uniques) > 10 else ""))
    
    # Compile context efficiently
    context = [
        f"Table Name: {table_name}",
        
        f"Shape: {df.shape[0]} rows × {df.shape[1]} columns",
        
        f"First 5 rows:\n{df_preview}",
        
        "Column Info:\n" + "\n".join(column_info),
        
        "Common Categorical Values:\n" + "\n".join(common_values),
        "Unique Values Summary:\n" + "\n".join(unique_values_summary),
        
        "Statistic Summary:\n" + "\n"+ (summary_stats.to_string()),
        
    ]

    if metadata_desc:
        context.insert(0, f"Metadata Description:\n{metadata_desc}")

    # Efficient Prompt
    prompt = (
        f"Your role is Zara, a sharp, experienced data analyst, project manager, and petroleum engineer in the oil and gas industry.\n"
        f"Your job is to answer user questions strictly based on the given dataset. Do not create or assume data.\n"
        f"Use markdown, be concise (1-3 sentences). If the question makes no sense, reply wittily.\n"
        f"Determine the user's intent based on their question: '{detect_intent(question)}'.\n\n"
        
        # f"Use only pandas for data analysis or tables and Plotly for charts.\n"
        
        # f"Generate Python code using pandas to create a DataFrame from a dataset stored in <df>.\n"
        # f"The result must be stored in <df_result>. Use only pandas.\n"
        
        # f"Generate Python code using Plotly to plot data from <df>.\n"
        # f"The plot must be stored in <fig>. Use only Plotly.\n"
        
        # f"The provided code must be wrapped in format: ```python <code>```\n"
        f"{question.strip()}\n\nContext:\n" + "\n\n".join(context)
    )

    return prompt