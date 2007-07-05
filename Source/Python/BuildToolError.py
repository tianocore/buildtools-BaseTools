class BuildToolError(Exception):
    def __init__(self, message):
        self.Message = message

    def __str__(self):
        return "ERROR: %s" % str(self.Message)

class AutoGenError(BuildToolError):
    def __init__(self, message):
        BuildToolError.__init__(self, message)

    def __str__(self):
        return "\nAutoGen: %s" % BuildToolError.__str__(self)

class GenFdsError(BuildToolError):
    def __init__(self, message):
        BuildToolError.__init__(self, message)

    def __str__(self):
        return "\nGenFds: %s" % BuildToolError.__str__(self)

if __name__ == "__main__":
    try:
        raise AutoGenError, "my fault"
    except BuildToolError, e:
        print e
    except Exception, e:
        print "Python:", e

    try:
        raise GenFdsError, "my fault"
    except BuildToolError, e:
        print e
    except Exception, e:
        print "Python:", e

    try:
        xyz = abc[1]
    except BuildToolError, e:
        print e
    except Exception, e:
        print "\nPython:", e
