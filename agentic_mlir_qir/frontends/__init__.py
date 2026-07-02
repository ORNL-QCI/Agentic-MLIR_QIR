"""Input frontends that convert non-MLIR source formats into MLIR.

The frontends produce MLIR text that the existing deterministic
``MLIRParser`` + ``QIRGenerator`` pipeline consumes unchanged. This keeps
alternative input formats (e.g. OpenQASM) flowing through "the same framework".
"""
