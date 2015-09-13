#! /usr/bin/env python2.7

# dependencies: llvm, termcolor

import os
from termcolor import colored, cprint
import sys

if __name__ == '__main__':
    exit('This must run from within lldb!')
import lldb

colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
colormap = dict()
coloridx = 0


def printLine(var, functionName, outfile):
    global colors
    global colormap
    global coloridx
    strm = lldb.SBStream()
    var.GetExpressionPath(strm)
    name = strm.GetData()
    val = var.GetValue()
    if val == None:
        #some vars, like structs, don't have values. Only their fields do!
        return
    typ = var.GetTypeName()
    size = var.GetByteSize()
    outfile.write('%s,%s,%s,%s,%i\n' % (functionName, name, val, typ, size))

    if val and val.startswith('0x'):
        if not val in colormap.keys():
            colormap[val] = colors[coloridx]
            coloridx = (coloridx + 1) % len(colors)
        val = colored(val, colormap[val])
    print '%20s = %-20s : %-10s (size = %-2i)' % (name, val, typ, size)


def showValue(var, functionName, outfile):
    printLine(var, functionName, outfile)


def showWithChildren(var, functionName, outfile):
    showValue(var, functionName, outfile)
    if var.MightHaveChildren():
        for i in range(0, var.GetNumChildren()):
            chld = var.GetChildAtIndex(i)
            if chld.TypeIsPointerType() and chld.GetValue() == None:
                continue
            #if chld.GetError():
            #print('child=%s' % str(chld))
            showWithChildren(chld, functionName, outfile)


def showOverview(var, functionName, outfile):
    showValue(var.AddressOf(), functionName, outfile)
    showWithChildren(var, functionName, outfile)


def showHeader(msg='', pattern='=', attrs=[]):
    assert len(pattern) == 1
    length = 70
    if msg != '':
        h = pattern + ' ' + colored(msg, 'white', attrs=attrs) + ' '
        h = h + pattern * (length - len(h))
        assert len(h) == length
        print(h)
    else:
        print(pattern * length)


def showLocalsOverview(thread, frameidx, outfile):
    functionName = thread.frame[frameidx].GetFunctionName()
    showHeader('FUN: ' + functionName, '-')

    localvars = thread.frame[frameidx].GetVariables(True, True, False, True)
    for var in localvars:
        showOverview(var, functionName, outfile)


def printStack(debugger, command, result, internalDict):
    with open('stack.dump', 'w') as outfile:
        if isinstance(debugger, lldb.SBDebugger):
            target = debugger.GetSelectedTarget()
            process = target.GetProcess()
            thread = process.GetSelectedThread()

            globalvars = thread.frame[0].GetVariables(False, False, True, True)

            showHeader('STACK')
            for i in range(0, len(thread.frame)):
                if (thread.frame[i].GetFunctionName() != 'start'):
                    showLocalsOverview(thread, i, outfile)

            showHeader('GLOBALS')

            for var in globalvars:
                showOverview(var, 'global', outfile)

            showHeader()

            return False


def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
        'command script add -f printStack.printStack printStack')
