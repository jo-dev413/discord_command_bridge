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


class CmdManager:

    """
    コマンドから処理を呼び出すクラス

    Attributes
    ----------
    cmds          : list
        CmdExporterでexportされた辞書を格納するリスト
    cmd_dict     : dict
        cmdsを結合した辞書オブジェクト
    bot_header   : boolean
        コマンド識別の際に他ボットとの競合を避けるために，
        ボット識別子を先頭につけるかどうか
    """

    def __init__(self):
        """
        コンストラクタ
        初期化処理、bot_headerはfalse
        """
        self.cmds = []
        self.cmd_dict = {}
        self.bot_header = False

    def enableBotHeader(self):
        """
        ボット識別子を先頭につける
        """
        self.bot_header = True

    def disableBotHeader(self):
        """
        ボット識別子を先頭につける
        """
        self.bot_header = False

    def add(self, cmd):
        """
        コマンド(dict)をcmdsに追加
        """
        self.cmds.append(cmd)

    def regist(self):
        """
        cmdsをcmd_dictへ連結
        """
        for cmd in self.cmds:
            self.cmd_dict.update(cmd.export())

    async def execute(self, client, event):
        """
        コマンドに紐づくクラスの抽象クラス

        Parameters
        ----------
        client : discord.Client
            discord.py で生成されるclient
        event  : client.event
            discord.py のclientから発火されるevent．ex. on_messageならmessage
        """
        # メッセージをパース
        perthed = self.perth(event.content)
        # コマンド識別子を取得
        cmd = self.cmd_dict[perthed[0]]
        # クラスアドレスを取得
        cmd_handler_class = cmd["class"]
        # クラスをインスタンス化
        handler_class = cmd_handler_class.get_instance(client, event)
        # optionに応じて対応したメソッドを呼び出す
        for i in range(2, len(perthed), 2):
            op = cmd["options"]
            handler_fun = op[perthed[i]]
            eval("handler_class."+handler_fun)(perthed[i+1])
        # デフォルトのメソッドを呼び出す
        await eval("handler_class."+cmd["default_handler"])(perthed[1])

    def perth(self, message_str):
        """
        コマンドに紐づくクラスの抽象クラス

        Parameters
        ----------
        message_str : str
            送信されたコマンド文字列

        Returns
        -------
        perthed : list
            分割されたコマンド文字列
            ex. ["example_cmd",["default_value_1","default_value_2"],["-p"],[],
            ["-t"],["-t_option_value"]]
        """
        perthed = []
        splited = [s for s in message_str.split()]

        if self.bot_header:
            splited.pop(0)
            perthed.append(splited.pop(0))
        else:
            perthed.append(splited.pop(0))

        tmp = []
        for s in splited:
            print(s)
            if s.startswith('-'):
                perthed.append(tmp)
                perthed.append(s)
                tmp = []
            else:
                tmp.append(s)
        perthed.append(tmp)
        return perthed
