import configparser
import string

_ConfigDefault = {
    "database.dbms":                "SQL Server",
    "database.server":              "localhost",
    "database.name":                "",
    "database.integratedsecurity":  "false",
    "database.user":                "root",
    "database.password":            ""
    }

def LoadConfig(file, config={}, getConfigFor="database"):
    """
    returns a dictionary with keys of the form
    <section>.<option> and the corresponding values
    """
    config = config.copy()
    cp = configparser.ConfigParser()
    cp.read(file)
    for sec in cp.sections():
        name = sec.lower()
        if name == getConfigFor:
            for opt in cp.options(sec):
                config[name + "." + opt.lower()] = cp.get(sec, opt)
    return config

if __name__=="__main__":
    print(LoadConfig("some.ini", _ConfigDefault))
