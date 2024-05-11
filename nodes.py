# NODES

class NumberNode:
    def __init__(self, token: str) -> None:
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"


class BinaryOperationNode:
    def __init__(self, left_node, operation_token: str, right_node) -> None:
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"


    