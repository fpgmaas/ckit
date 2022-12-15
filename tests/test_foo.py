def test_foo():
    def foo():
        return "foo"

    assert foo() == "foo"
