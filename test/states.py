from __future__ import annotations


class TestState:
    """TestState."""

    def __init__(
        self,
        data: dict[str, any] = None,
        responses: dict[str, any] = None,
        messages: dict[str, any] = None,
    ):
        self.data = data if data is not None else {}
        self.responses = responses if responses is not None else {}
        self.messages = messages if messages is not None else {}

    def __add__(self, other: TestState) -> TestState:
        """__add__.

        Args:
            other (TestState): other

        Returns:
            TestState:
        """
        state = TestState(
            data=self.data | other.data,
            responses=self.responses | other.responses,
            messages=self.messages | other.messages,
        )
        return state

    def __iadd__(self, other: TestState) -> TestState:
        """__iadd__.

        Args:
            other (TestState): other

        Returns:
            TestState:
        """
        self.data = self.data | other.data
        self.responses = self.responses | other.responses
        self.messages = self.messages | other.messages
        return self

    def __eq__(self, other: TestState) -> bool:
        """__eq__.

        Args:
            other (TestState): other

        Returns:
            bool:
        """
        return (
            self.data == other.data
            and self.responses == other.responses
            and self.messages == other.messages
        )

    def __str__(self) -> str:
        """__str__.

        Args:

        Returns:
            str:
        """
        return f"TestState(\n\tdata={self.data},\n\tresponses={self.responses},\n\tmessages={self.messages}\n)"
