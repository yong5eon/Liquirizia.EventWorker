# -*- coding: utf-8 -*-

from Liquirizia.System.Util import GetHostName, GetProcessId, GenerateUUID

__all__ = (
	'GetNodeName',
)


def GetNodeName(id=None, prefix=None):
	fmt = '{host}.{id}.{uid}'

	if prefix:
		fmt = '{prefix}.' + fmt

	return fmt.format(
		prefix=prefix,
		host=GetHostName(),
		id=id if id else GetProcessId(),
		uid=GenerateUUID()
	)
