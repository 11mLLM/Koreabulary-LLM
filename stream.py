import streamlit as st
from page_builder import page_builder
def local_css(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="프롬프트 엔지니어링 용어집",
        page_icon="📜",
        menu_items={
            "Report a bug": "https://github.com/11mLLM/Koreabulary-LLM/issues"
        },
    )
    st.header("프롬프트 엔지니어링 용어집", divider="gray")
    builder = page_builder()
    menu = builder.menu   
    local_css("style.css") 
    columns = st.columns(len(menu))

    # Default choice
    choice = st.session_state.get('choice', 'All')

    for i, item in enumerate(menu):
        if columns[i].button(item):
            choice = item
            st.session_state.choice = item

    st.subheader(choice)
    vocab_data = builder.get_vocab_data(choice)


    with st.sidebar:
        options = st.multiselect(
            "키워드로 찾기",
            ["기술 용어", "알고리즘", "언어모델", "언어모델 튜닝 용어", "위험", "인공지능", "인공지능 방법론", "일반 용어", "프롬프트 엔지니어링", "기법"],
            placeholder="키워드 선택",
        )
    if options:
        vocab_data = {k: v for k, v in vocab_data.items() if any(tag in v['Tag'] for tag in options)}

    for term, details in vocab_data.items():
        with st.expander(f"**{details['Target']}** :gray[| {term}]"):
            # Targets and Tags
            tag_html = ""
            for tag in details['Tag']:
                tag_class = tag.replace(" ", "-")
                tag_html += f'<div class="tag-container tag-{tag_class}" style="margin-left: 5px;">{tag}</div>'   
            st.markdown(f'''
                    <div style="display: flex; align-items: center;">{tag_html}</div>
            ''', unsafe_allow_html=True)
            
            # Examples and URLs
            try:
                st.markdown("---")
                st.write("**Example:**")
                for example, url in zip(details['Example'], details['URL']):
                    st.markdown(f'''
                    <div class="example-text">
                        {example}
                        <a class="example-link" href="{url}" target="_blank">[원문 보기]</a>
                    </div>''', unsafe_allow_html=True)
            except:
                None
            st.markdown("&nbsp;")

if __name__ == '__main__':
    main()

