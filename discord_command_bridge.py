# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class CmdBase(metaclass=ABCMeta):
    """
    コマンドに紐づくクラスの抽象クラス

    Attributes
    ----------
    client : discord.Client
        discord.py で生成されるclient
    event  : client.event
        discord.py のclientから発火されるevent．ex. on_messageならmessage
    """

    def __init__(self, client, event):
        """
        コンストラクタ

        Parameters
        ----------
        client : discord.Client
            discord.py で生成されるclient
        event  : client.event
            discord.py のclientから発火されるevent．ex. on_messageならmessage
        """
        self.client = client
        self.event = event

    @abstractmethod
    def get_instance(self, client, event):
        """
        インスタンスを生成して返す

        Parameters
        ----------
        client : discord.Client
            discord.py で生成されるclient
        event  : client.event
            discord.py のclientから発火されるevent．ex. on_messageならmessage

        Returns
        -------
        cmd : Extended class
            このクラスのインスタンス
        """
        pass


class CmdExporter:
    """
    コマンドをdictへ変換するクラス

    Attributes
    ----------
    op          : dict
        オプションとそれに対応するメソッド名
    cmd_str     : str
        コマンド文字列
    cmd_class   : CmdBase
        コマンドを処理するクラスアドレス
    cmd_default : str
        必ず最後に実行される非同期メソッド名
    """

    def __init__(self, cmd_str, cmd_class, default_handler_name="default"):
        """
        コンストラクタ
        初期化とデフォルトのコマンドハンドラーを定義

        Parameters
        ----------
        cmd_str     : str
            コマンド文字列
        cmd_class   : CmdBase
            コマンドを処理するクラスアドレス
        cmd_default : str
            デフォルトはdefault
            必ず最後に実行される非同期メソッド名
        """
        self.op = {}
        self.cmd_str = cmd_str
        self.cmd_class = cmd_class
        self.cmd_default = default_handler_name

    def set_opt(self, opt_key, handler_func):
        """
        オプションのハンドラーを定義

        Parameters
        ----------
        opt_key     : str
            オプション文字列
        handler_func : str
            オプションが付与されたときに呼ばれるメソッド名
        """
        self.op[opt_key] = handler_func

    def export(self):
        """
        コマンドと処理の関係を辞書型で返す

        return example
        {
            "class" : class address,
            "default_handler" : "default handler name",
            "options" : {
                "-t" : "func_name_1",
                "-m" : "func_name_2",
            }
        }

        Returns
        -------
        cmd : dict
            コマンドと処理を結び付けた辞書オブジェクト
        """
        export_value = {}
        export_value["class"] = self.cmd_class
        export_value["default_handler"] = self.cmd_default
        export_value["options"] = self.op
        return {self.cmd_str: export_value}
