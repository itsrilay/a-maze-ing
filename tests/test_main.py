from package.main import hello_world


def test_hello_world():
    """
    A basic test to ensure the template CI passes out of the box.
    Users should delete or modify this test.
    """
    result = hello_world()
    assert result == "Hello from the template!"
