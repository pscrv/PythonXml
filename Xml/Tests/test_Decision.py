from Xml.Decision import Decision, DuplicateTagError, Tags


text = '<Decision> Nothing </Decision>'

def _makeValidDecision () :
    decision = Decision( '' )
    for tag in Tags :
        decision.AddTag( tag, 'anything' )
    return decision


def test__Constructor () :
    decision = Decision( text )
    assert decision._rawString == text


def test_HasTag () :
    decision = Decision( text )
    assert decision.HasTag( 'Decision' )
    assert decision.HasTag( 'NotATag' ) == False, 'decision should not have a tag <NotATag>'



def test_GetTag () :
    decision = Decision( text )
    assert decision.GetTag( 'Decision' ) == ' Nothing '


def test_AddTag () :
    tag = 'Tail'
    content = 'Stripey'
    decision = Decision( text )
    decision.AddTag( tag, content )
    found = decision.GetTag( tag )
    assert found == content


def test_GetDecision () :
    decision = Decision( text )
    found = decision.GetDecision()
    assert found == f'<Decision>\n{text}</Decision>\n'


def test_NoDuplicateTags () :
    decision = Decision( text )
    decision.AddTag( 'Tail', 'first' )
    try :
        decision.AddTag( 'Tail', 'second' )
        assert False, 'Decision.AddTag failed to throw a DuplicateTagError exception.'
    except DuplicateTagError :
        assert True

def test_HasAllValidTags () :
    invalidDecision = Decision( text )
    assert invalidDecision.HasAllValidTags() == False, 'decision should have no valid tags'

    validDecision = _makeValidDecision()
    assert validDecision.HasAllValidTags()


def test_HasOnlyValidTags () :
    invalidDecision = Decision( text )
    assert invalidDecision.HasOnlyValidTags() == False

    validDecision = _makeValidDecision()
    assert validDecision.HasOnlyValidTags()



