"""
メインのプログラムです。
streamlitがインストールされていることを確認してから実行してください。
"""

import sys
import os
import unicodedata

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logic.game import QuizLogic  # noqa: E402


def normalize_input(text: str) -> str:
    """ 全角と半角を区別しないように統一 """
    return unicodedata.normalize("NFKC", text)


# --- UI設定 ---
st.set_page_config(page_title="Hit & Blow", page_icon="🎯")

# --- サイドバー: 遊び方の追加 ---
with st.sidebar:
    st.header("🎮 遊び方")
    with st.expander("クリックしてルールを表示"):
        st.write(
            """
        ### Hit & Blow ルール：
        1. 🤖 **コンピュータがランダムな数字を生成します。**
        2. 🤔 **数字を予想して入力し、送信ボタンを押します。**
        3. 💬 **ヒットとブローの結果が表示されます。**
            - **Hit:** 数字も位置も一致
            - **Blow:** 数字は一致するが位置が異なる
        4. 💪 **指定回数以内に正解を目指してください！**
        """
        )

    # ゲーム設定
    digit = st.number_input("桁数", min_value=1, max_value=10, value=3)
    max_challenge = st.number_input("挑戦回数", min_value=1, value=10)

    if st.button("ゲーム開始"):
        quiz = QuizLogic(digit, max_challenge)
        quiz.create_ans()
        st.session_state["quiz"] = quiz
        st.session_state["history"] = []
        st.session_state["game_over"] = False
        st.session_state["result_message"] = ""

# --- メイン画面 ---
st.title("🎯 Hit & Blow ゲーム")

# ゲームの状態を管理
if "quiz" in st.session_state:
    quiz = st.session_state["quiz"]
    is_game_over = st.session_state.get("game_over", False)

    # メッセージの表示
    if "result_message" in st.session_state:
        st.markdown(st.session_state["result_message"], unsafe_allow_html=True)

    # 入力欄 & 送信ボタン（ゲームオーバー時は無効化）
    guess = st.text_input("数字を入力してください", disabled=is_game_over)
    guess = normalize_input(guess) if guess else ""

    send_button = st.button("送信", disabled=is_game_over)

    if send_button and not is_game_over:
        if not guess:
            st.error("⚠️ 入力されていません！")
        else:
            result = quiz.input_check(guess)
            if result == "ok":
                quiz.user_str = guess
                hit = quiz.hit_count()
                blow = quiz.blow_count()
                st.session_state["history"].append((guess, hit, blow))

                if hit == digit:
                    st.session_state["result_message"] = """
                    <h4 style='color: #4CAF50; text-shadow: 2px 2px 4px #333;'>🎉 正解しました！おめでとうございます！</h4>
                    <p style='font-size: 16px;'>🎮 <b>サイドバーからもう一度挑戦できるよ!</b></p>
                    """
                    st.session_state["game_over"] = True
                    st.rerun()

                elif quiz.count + 1 > max_challenge:
                    st.session_state["result_message"] = """
                    <h4 style='color: #FF5252; text-shadow: 2px 2px 4px #333;'>😢 挑戦回数超過！ゲームオーバーです。</h4>
                    <p style='font-size: 16px;'>🎮 <b>サイドバーから再挑戦してみよう!</b></p>
                    """
                    st.session_state["game_over"] = True
                    st.rerun()

                else:
                    quiz.count += 1
                    st.rerun()

            else:
                st.error(result)  # 無効な入力はリロードしない

    # プレイ履歴
    st.subheader("📜 プレイ履歴")
    for i, attempt in enumerate(st.session_state["history"], start=1):
        st.markdown(
            f"""
            <p style='font-size: 18px; font-weight: bold;'>
            {i}. 入力: {attempt[0]} → Hit: {attempt[1]}, Blow: {attempt[2]}</p>
        """,
            unsafe_allow_html=True,
        )

else:
    st.warning("サイドバーからゲームを開始してください。")
