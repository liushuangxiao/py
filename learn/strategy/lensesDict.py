def ageToString(age):
    switcher = {
        '1': "young",
        '2': "pre-presbyopic",
        '3': "presbyopic",
    }
    return switcher.get(age, age)


def spectacleToString(spectacle):
    switcher = {
        '1': "myope",
        '2': "hypermetrope",
    }

    return switcher.get(spectacle, spectacle)


def astigmaticToString(astigmatic):
    switcher = {
        '1': "no",
        '2': "yes",
    }

    return switcher.get(astigmatic, astigmatic)


def tearToString(tear):
    switcher = {
        '1': "reduced",
        '2': "normal",
    }

    return switcher.get(tear, tear)

def classToString(cla) :
    switcher = {
        '1' : "hard",
        '2' : "soft",
        '3' : "no",
    }

    return switcher.get(cla, cla)