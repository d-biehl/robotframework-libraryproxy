# CHANGELOG

## v0.3.0 (2024-08-02)

### Chore

* chore: fix imports sortings ([`d96956f`](https://github.com/d-biehl/robotframework-libraryproxy/commit/d96956fed755c7b834e4c668e05134503bd993a8))

* chore: fix RF versions in workflow ([`ccc764c`](https://github.com/d-biehl/robotframework-libraryproxy/commit/ccc764c37fc9ef858dab08e6374e25947cf658b7))

* chore: fix artifact names and disable flake8 ([`1fbfbc1`](https://github.com/d-biehl/robotframework-libraryproxy/commit/1fbfbc1a085639f8dec4b63c50e5bde7d732a7fe))

* chore: update python and RF versions in workflow ([`1faf0ab`](https://github.com/d-biehl/robotframework-libraryproxy/commit/1faf0ab71357a1eadd67bb6a3d2923226515a746))

* chore: fix some quality things ([`de02ba8`](https://github.com/d-biehl/robotframework-libraryproxy/commit/de02ba892ea71b5a10ff309d71cc28020749e3d8))

* chore: enable workflow dispatch ([`3636dc7`](https://github.com/d-biehl/robotframework-libraryproxy/commit/3636dc7d6ede8d26921bd855edfbc44aaf8b2410))

* chore: update git actions ([`612c60f`](https://github.com/d-biehl/robotframework-libraryproxy/commit/612c60fc638d960031a30f7ce2f21908673d745c))

### Feature

* feat: support for RF7 ([`e71598a`](https://github.com/d-biehl/robotframework-libraryproxy/commit/e71598a143b8c4abeb9d54bc1416151aca476d6f))

## v0.2.0 (2022-12-15)

### Chore

* chore: update packages ([`50c2765`](https://github.com/d-biehl/robotframework-libraryproxy/commit/50c2765a1bb455a9bfe23c7dadd789472addfbbb))

* chore: fix some mypy warnings ([`d0a794b`](https://github.com/d-biehl/robotframework-libraryproxy/commit/d0a794b409c569f03ab0d51b9a0152dfd45b4434))

* chore: update gitignore ([`2c78ff8`](https://github.com/d-biehl/robotframework-libraryproxy/commit/2c78ff888482261ef1bc06b8135e5d3e8394d28b))

### Feature

* feat: call keywords with real args, do not convert it to strings

keyword methods/functions are now called directly, not via robot conversion. This allows you to use the normal parameters as you would call the python funtion directly ([`36c8aa3`](https://github.com/d-biehl/robotframework-libraryproxy/commit/36c8aa3620b19f1d8ec4a07220382be944ca727d))

### Test

* test: fix tests ([`bc1839b`](https://github.com/d-biehl/robotframework-libraryproxy/commit/bc1839bfe5e85da4e17e1246ec90cf76cfc09646))

## v0.1.1 (2022-11-25)

### Chore

* chore: update .github workflow ([`7a9c6b2`](https://github.com/d-biehl/robotframework-libraryproxy/commit/7a9c6b27c868182a45865f51252f7bde850772c0))

* chore: update .github workflow ([`6bafecf`](https://github.com/d-biehl/robotframework-libraryproxy/commit/6bafecf767e3e0c8faf1682ddbb1219321ee250e))

* chore: update .github workflow ([`5832a8c`](https://github.com/d-biehl/robotframework-libraryproxy/commit/5832a8ca168caa56feb0b386b37fdeba06157283))

* chore: update .github workflow ([`9544f7d`](https://github.com/d-biehl/robotframework-libraryproxy/commit/9544f7df9bcb8a4204c1e94b77b90ef9a6869092))

* chore: revert ([`f1e4eeb`](https://github.com/d-biehl/robotframework-libraryproxy/commit/f1e4eebad3625fcdf87d4aa54c28b2d6bdbf7505))

* chore: update packages ([`f4bd769`](https://github.com/d-biehl/robotframework-libraryproxy/commit/f4bd7697d3dc6e18587d4e0565dce3607d98a472))

* chore: packages ([`915407d`](https://github.com/d-biehl/robotframework-libraryproxy/commit/915407dab3bc88771e017d88027a2eafbfaf48c2))

* chore: fix .github workflows ([`499d310`](https://github.com/d-biehl/robotframework-libraryproxy/commit/499d31031d93becc7f32b84e78485f3e8f5a6e6e))

* chore: correct .github workflow ([`b3b4209`](https://github.com/d-biehl/robotframework-libraryproxy/commit/b3b420933e15f91714d8d3570f22bfac52932cb6))

* chore: update github workflows ([`7d175bb`](https://github.com/d-biehl/robotframework-libraryproxy/commit/7d175bb434ebed7cda925eec0a831ac4a7977d42))

* chore: update .github workflows ([`3b10d33`](https://github.com/d-biehl/robotframework-libraryproxy/commit/3b10d3303dc7b23194f45c3ed046b8552df88f39))

* chore: setup .github folder ([`7b608d4`](https://github.com/d-biehl/robotframework-libraryproxy/commit/7b608d4f83aca993d2bd48106395a32d864fd15a))

### Fix

* fix: tests ([`fbd6586`](https://github.com/d-biehl/robotframework-libraryproxy/commit/fbd65863e00238e39e81756745e69e3193a777b4))

* fix: tests ([`51f434f`](https://github.com/d-biehl/robotframework-libraryproxy/commit/51f434ff72ffe451b9407bdb6018ac3055a2f9ae))

* fix: some code mypy smells ([`99b6150`](https://github.com/d-biehl/robotframework-libraryproxy/commit/99b615063d5006078d53ca8d0929277b55b7849a))

## v0.1.0 (2022-11-25)

### Feature

* feat: use type hints to get library name

```python
class TestClass:
    builtin: BuiltIn = library_proxy()
``` ([`b10f9f9`](https://github.com/d-biehl/robotframework-libraryproxy/commit/b10f9f9b0aafd254e5c44f167b40eb10b77348fd))

## v0.0.2 (2022-11-25)

## v0.0.1 (2022-11-25)

### Build

* build: add semantic versioning ([`41f3246`](https://github.com/d-biehl/robotframework-libraryproxy/commit/41f3246914fd3520dc1151038a1df0af38fc30c4))

### Unknown

* switch to pep404 ([`210cd6b`](https://github.com/d-biehl/robotframework-libraryproxy/commit/210cd6bae9c64f99d015d0d29c51efc3911e1169))

* add dynamic versioning ([`ab5288d`](https://github.com/d-biehl/robotframework-libraryproxy/commit/ab5288d15674a7b6a1fa4d29ceb09d40456a427a))

* add some more tests ([`8edb73a`](https://github.com/d-biehl/robotframework-libraryproxy/commit/8edb73a2f75b0076212151119cfd20c5619a24b8))

* correct .gitignore ([`22934e2`](https://github.com/d-biehl/robotframework-libraryproxy/commit/22934e2c0695401b3255466bd02e84d9047d052e))

* update README ([`66732cb`](https://github.com/d-biehl/robotframework-libraryproxy/commit/66732cbeb11bc94361921c9836b24c126d758d24))

* update pyproject ([`cdfe332`](https://github.com/d-biehl/robotframework-libraryproxy/commit/cdfe332ec0ee6260a2662256bd64ed4eb2f7ec21))

* Merge branch &#39;master&#39; of https://github.com/d-biehl/robotframework-libraryproxy ([`cd1b19e`](https://github.com/d-biehl/robotframework-libraryproxy/commit/cd1b19e90ed143df2b62e0ac1491428528d1bef9))

* Create LICENSE ([`2198d40`](https://github.com/d-biehl/robotframework-libraryproxy/commit/2198d40895619739d1e94a6781d8b3fb46b2c5be))

* Update README.md ([`07a441c`](https://github.com/d-biehl/robotframework-libraryproxy/commit/07a441ca1ed89f2bcdbdc8e28eadd286ed92edd4))

* update packages ([`cd7f5b5`](https://github.com/d-biehl/robotframework-libraryproxy/commit/cd7f5b54220d9bfaab97c4eb6e74c5c048775c12))

* Create CODE_OF_CONDUCT.md ([`a791a9f`](https://github.com/d-biehl/robotframework-libraryproxy/commit/a791a9faf924f774b17191bee964ae74f80f537f))

* add some text to readme ([`5399aae`](https://github.com/d-biehl/robotframework-libraryproxy/commit/5399aaee0e24ac38ea5cbfe8b3471cf31d20ace6))

* first commit ([`90c655e`](https://github.com/d-biehl/robotframework-libraryproxy/commit/90c655e69d14d4c13701e5b2f6eea1f11753229e))
