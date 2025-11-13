template = """
Language: {{ language }}
Question: {{ question }}
"""

language = "en"
template = f"""
Language: {language},
Question: {{{{ question }}}}
"""