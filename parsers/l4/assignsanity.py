import astdef

def identName(ident):
    if isinstance(ident, astdef.IdentifierVar):
        return ident.vname
    else:
        return ident.arrname

def verifyComponent(com, piv, nothrow):
    if isinstance(com, astdef.CommandAssign):
        piv.update({identName(com.ident)})

    if isinstance(com, astdef.CommandRead):
        piv.update({identName(com.ident)})

    if not nothrow:
        if isinstance(com, astdef.ValueVar):
            if identName(com.ident) not in piv:
                raise astdef.ProgramError("Program Error:\n Never touched variable servig as value:\nLine: {0}, Name: {1}".format(com.det, identName(com.ident)))

        if isinstance(com, astdef.IdentifierArrVar):
            if com.vname not in piv:
                raise astdef.ProgramError("Program Error:\n Never touched variable servig as index:\nLine: {0}, Name: {1}".format(com.det, com.vname))


def unwindCommand(com, piv, nothrow):
    if hasattr(com, "children"):
        for chld in com.children:
            if isinstance(chld, list):
                pass
            else:
                unwindCommand(chld, piv, nothrow)
    verifyComponent(com, piv, nothrow)
    if hasattr(com, "children"):
        for chld in com.children:
            if isinstance(chld, list):
                res = verifyCommands(piv, chld, nothrow)
                piv.update(res)
            else:
                pass

def verifyCommands(possiblyInitialized, commands, nothrow):
    piv = possiblyInitialized.copy()
    for ci in commands:
        if isinstance(ci, astdef.CommandIf):
            unwindCommand(ci.condition, piv, nothrow)
            pit = verifyCommands(piv, ci.trueCommands, nothrow)
            if ci.falseCommands == None:
                pif = piv.copy()
            else:
                pif = verifyCommands(piv, ci.falseCommands, nothrow)
            piv.update(pit)
            piv.update(pif)
        elif isinstance(ci, astdef.CommandFor):
            unwindCommand(ci.startval, piv, nothrow)
            unwindCommand(ci.endval, piv, nothrow)
            tempscope = piv.copy()
            tempscope.update({ci.itername})
            if not hasattr(ci, "addedVars"):
                res = verifyCommands(tempscope, ci.commands, True)
                ci.addedVars = True
                res.difference_update({ci.itername})
                piv.update(res)
                tempscope.update(res)
            if not nothrow:
                verifyCommands(tempscope, ci.commands, nothrow)
        elif isinstance(ci, astdef.CommandWhile):
            unwindCommand(ci.condition, piv, nothrow)
            if not hasattr(ci, "addedVars"):
                res = verifyCommands(piv, ci.commands, True)
                ci.addedVars = True
                piv.update(res)
            if not nothrow:
                verifyCommands(piv, ci.commands, nothrow)
        elif isinstance(ci, astdef.CommandRepeat):
            unwindCommand(ci.condition, piv, nothrow)
            if not hasattr(ci, "addedVars"):
                res = verifyCommands(piv, ci.commands, True)
                ci.addedVars = True
                piv.update(res)
            if not nothrow:
                verifyCommands(piv, ci.commands, nothrow)
        else:
            unwindCommand(ci, piv, nothrow)
    return piv

def checkProgram(prog):
    possiblyInitialized = set()
    curcommands = prog.commands
    verifyCommands(possiblyInitialized, curcommands, False)



