"""
ゲームの処理をします
"""
import random
from datetime import datetime
from pathlib import Path


class QuizLogic:
    def __init__(self, digit: int, max_challenge: int) -> None:
        self.digit = digit  # 桁数
        self.max_challenge = max_challenge  # 入力できる回数
        self.ans_str = ""  # あてる数字
        self.user_str = ""  # ユーザの解答
        self.count = 1  # カウント回数の初期化
        self.clear = False  # クリアしたかどうか
        self.log = []  # ログ
        self.exit = False  # 終了フラグ

    def create_ans(self) -> str:
        """正解の生成をする

        Returns:
            str: 正解の数字
        """
        while True:
            ans_num = random.randint(0, 9)
            # 数字が重複していないか
            if str(ans_num) in self.ans_str:
                continue
            self.ans_str += str(ans_num)
            # 指定した桁数分生成したか
            if len(self.ans_str) == self.digit:
                break
        return self.ans_str

    def input_check(self, input_data: str) -> str:
        """入力値の検証とエラーメッセージを返す

        Args:
            input_data (str): 入力された数値

        Returns:
            str: 成功時は'ok'を返し、エラー時はエラーメッセージを返す
        """
        if not input_data.isdigit():
            return '⚠️ 数字を入力してください'

        if len(input_data) != self.digit:
            return f'⚠️ {self.digit}桁で入力してください'

        if len(set(input_data)) != self.digit:
            return '⚠️ 重複しない数字を使用してください'

        return 'ok'

    def hit_count(self) -> int:
        """ hit(数字と桁位置の両方が同じ)の回数をカウントするメソッド

        Returns:
            int: hitの回数
        """
        hit = 0
        for answer, user in zip(self.ans_str, self.user_str):
            if answer == user:
                hit += 1  # hitの回数をカウントアップ
        return hit

    def blow_count(self) -> int:
        """blow(数字のみ同じ)の回数をカウントするメソッド

        Returns:
            int: blowの回数
        """
        hit = self.hit_count()
        blow = 0
        for digit in self.user_str:
            if digit in self.ans_str:
                blow += 1  # blowの回数をカウントアップ
        blow -= hit  # hitの回数分を引く
        return blow
