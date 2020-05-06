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
            対象の果物の値段。
        """
        pass
