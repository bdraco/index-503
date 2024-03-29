# Changelog

<!--next-version-placeholder-->

## v2.5.1 (2023-09-29)

### Fix

* Canonicalize paths in the index ([#59](https://github.com/bdraco/index-503/issues/59)) ([`331d42a`](https://github.com/bdraco/index-503/commit/331d42af912e300815ff211aff387d8869c6faa5))

## v2.5.0 (2023-09-29)

### Feature

* Handle wheel files changing ([#58](https://github.com/bdraco/index-503/issues/58)) ([`183e27c`](https://github.com/bdraco/index-503/commit/183e27c82b29ef5d43ae8ddbf7b608a265f82cd3))

## v2.4.1 (2023-09-21)

### Fix

* Ensure index is always built with readable permissions ([#56](https://github.com/bdraco/index-503/issues/56)) ([`7884985`](https://github.com/bdraco/index-503/commit/78849859545d1278d877577abffd432a631a0ab0))

## v2.4.0 (2023-07-15)

### Feature

* Remove pip workarounds ([#51](https://github.com/bdraco/index-503/issues/51)) ([`13853b1`](https://github.com/bdraco/index-503/commit/13853b1e4b335cddfd3ef1ef5336ce5ebfb5bd49))

## v2.3.1 (2023-06-02)
### Fix

* Document pip name compare problems ([#49](https://github.com/bdraco/index-503/issues/49)) ([`ea9e7d6`](https://github.com/bdraco/index-503/commit/ea9e7d638b70ab1dee1cea2eb61eac95cebbb890))

## v2.3.0 (2023-06-02)
### Feature

* Add example pip usage to the docs ([#48](https://github.com/bdraco/index-503/issues/48)) ([`0910704`](https://github.com/bdraco/index-503/commit/0910704a46f4b7eaeec530469f021b3e8dcf955e))

## v2.2.0 (2023-06-02)
### Feature

* Speed up metadata creation when there is a cache ([#47](https://github.com/bdraco/index-503/issues/47)) ([`a33c45f`](https://github.com/bdraco/index-503/commit/a33c45f8d8dce9a0ba1d6e62194530f2b8a31de1))

## v2.1.1 (2023-06-02)
### Fix

* Remove unused code ([#46](https://github.com/bdraco/index-503/issues/46)) ([`a023b79`](https://github.com/bdraco/index-503/commit/a023b7964f6c8653614caf688c52fb978994d7dd))

## v2.1.0 (2023-06-01)
### Feature

* Add tests for exclusive_lock ([#42](https://github.com/bdraco/index-503/issues/42)) ([`7d8395c`](https://github.com/bdraco/index-503/commit/7d8395cec229325b4eaca91e3a952dba505b3b0a))

### Fix

* Util test did not sleep long enough for slow runner ([#45](https://github.com/bdraco/index-503/issues/45)) ([`e82ed20`](https://github.com/bdraco/index-503/commit/e82ed20906a0494af723a8636e89c50eda8eada5))
* Util test did not sleep long enough for slow runner ([#44](https://github.com/bdraco/index-503/issues/44)) ([`5e97bda`](https://github.com/bdraco/index-503/commit/5e97bda7f59505399d38cddbd1f6980aef1a5bb5))
* Add missing cover for file ([#43](https://github.com/bdraco/index-503/issues/43)) ([`761fe3e`](https://github.com/bdraco/index-503/commit/761fe3e1c31b7a012c137c43dbe6fc30b4ab88d1))

## v2.0.0 (2023-06-01)
### Fix

* Drop python 3.8 support ([#39](https://github.com/bdraco/index-503/issues/39)) ([`8ada082`](https://github.com/bdraco/index-503/commit/8ada0828d42c732282ce771ead90baaf8c7dc6d1))
* Tests need to work on case sensitive fs ([#38](https://github.com/bdraco/index-503/issues/38)) ([`9377df0`](https://github.com/bdraco/index-503/commit/9377df008ebce3683e7e59ec932ad4a95b4a4cf6))
* Temp dir handling on older python ([#37](https://github.com/bdraco/index-503/issues/37)) ([`eea3ea3`](https://github.com/bdraco/index-503/commit/eea3ea37da8967e70cd32cf5ba2aa87f6a4379fd))

### Breaking

* python 3.8 support is removed ([`8ada082`](https://github.com/bdraco/index-503/commit/8ada0828d42c732282ce771ead90baaf8c7dc6d1))

## v1.0.0 (2023-06-01)
### Feature

* Refactor to make more testable ([#27](https://github.com/bdraco/index-503/issues/27)) ([`9c0560a`](https://github.com/bdraco/index-503/commit/9c0560aeb471f6740f145b6a2bb0b8342755dcf1))

### Fix

* More py3.8 typing fixes ([#31](https://github.com/bdraco/index-503/issues/31)) ([`8839d55`](https://github.com/bdraco/index-503/commit/8839d559b578626c0d0b6db03f8fd739cd69ac7b))
* Legacy typing for py3.8 ([#29](https://github.com/bdraco/index-503/issues/29)) ([`acf87a7`](https://github.com/bdraco/index-503/commit/acf87a7204e9969115358d63a190640eaa9ce940))

### Breaking

* Drop python 3.7 support ([`9c0560a`](https://github.com/bdraco/index-503/commit/9c0560aeb471f6740f145b6a2bb0b8342755dcf1))

## v0.2.2 (2023-06-01)
### Fix

* Split cache into its own module ([#23](https://github.com/bdraco/index-503/issues/23)) ([`c5356af`](https://github.com/bdraco/index-503/commit/c5356af842bcf556157553ff86c0451922ea2cc7))

## v0.2.1 (2023-06-01)
### Fix

* Cleanup cache side effects ([#22](https://github.com/bdraco/index-503/issues/22)) ([`9f1e7d1`](https://github.com/bdraco/index-503/commit/9f1e7d1af5c5d52884080e5e565d7d605e6bd7fb))

## v0.2.0 (2023-06-01)
### Feature

* Hold an exclusive lock to prevent multiple instances ([#21](https://github.com/bdraco/index-503/issues/21)) ([`25f661a`](https://github.com/bdraco/index-503/commit/25f661a5603224f91e3604b3b80b5c6357d1028a))

## v0.1.8 (2023-06-01)
### Fix

* Small cleanups ([#20](https://github.com/bdraco/index-503/issues/20)) ([`62933c1`](https://github.com/bdraco/index-503/commit/62933c14f7ead15fcb2332fce4ee8e3269cca8f0))

## v0.1.7 (2023-06-01)
### Fix

* Ensure new wheels can be found ([#19](https://github.com/bdraco/index-503/issues/19)) ([`441da84`](https://github.com/bdraco/index-503/commit/441da8446f7492bc81c8a26b5f04bf1567e21f94))

## v0.1.6 (2023-06-01)
### Fix

* Repair should always update the original_name to the metadata_name ([#7](https://github.com/bdraco/index-503/issues/7)) ([`a491882`](https://github.com/bdraco/index-503/commit/a491882da721232efdb2b8d1a66dec44ba03433c))

## v0.1.5 (2023-06-01)
### Fix

* Canonicalize_name in repairs ([#6](https://github.com/bdraco/index-503/issues/6)) ([`12be36a`](https://github.com/bdraco/index-503/commit/12be36a6bcb7d64867e717e8aca0fd875562eab6))

## v0.1.4 (2023-06-01)
### Fix

* Legacy typing ([#5](https://github.com/bdraco/index-503/issues/5)) ([`3847fc3`](https://github.com/bdraco/index-503/commit/3847fc342235c81cb9b94c90c366b63215ab7c0f))
* Caching ([#4](https://github.com/bdraco/index-503/issues/4)) ([`a303767`](https://github.com/bdraco/index-503/commit/a3037676d79fb59b0694745161b00a8f74251a39))

## v0.1.3 (2023-06-01)
### Fix

* Rebuild hash if metadata is updated ([#3](https://github.com/bdraco/index-503/issues/3)) ([`915d65b`](https://github.com/bdraco/index-503/commit/915d65bc821de15b055f7aad2326c781cbd633b4))

## v0.1.2 (2023-06-01)
### Fix

* Load names from cache ([#2](https://github.com/bdraco/index-503/issues/2)) ([`ee2ccf7`](https://github.com/bdraco/index-503/commit/ee2ccf7c5eed26266ab33a5a81c8a9df6347ff2b))

## v0.1.1 (2023-06-01)
### Fix

* Normalize names in metadata ([#1](https://github.com/bdraco/index-503/issues/1)) ([`fcb1bd7`](https://github.com/bdraco/index-503/commit/fcb1bd74416137779749b2b5d0bfdd057dde7590))

## v0.1.0 (2023-05-31)
### Feature

* Init ([`72de6e5`](https://github.com/bdraco/index-503/commit/72de6e5f34d292ec190374273e10283b83d0bfda))

### Fix

* Readme ([`4c1f324`](https://github.com/bdraco/index-503/commit/4c1f324ceaec25b21b3273d0473fd488f2de1f84))
* Readme ([`7385204`](https://github.com/bdraco/index-503/commit/738520423add3f6ac4d6a0629f19f0ade3a0ab83))
* Typing ([`3bc1549`](https://github.com/bdraco/index-503/commit/3bc154989cebecc5864ddeab52aefd2e5161cb95))
* Ci ([`4584c36`](https://github.com/bdraco/index-503/commit/4584c368b8380d4f6eed7756642c03adda83db83))
* Ci ([`00f8812`](https://github.com/bdraco/index-503/commit/00f8812786bf8f43b8395a5209d5811b27fd752e))
* Ci ([`3fab19e`](https://github.com/bdraco/index-503/commit/3fab19eefccc157bc5686ae1686a78d9dc17e1f9))
* Fix ([`1dc7b79`](https://github.com/bdraco/index-503/commit/1dc7b791d2a2d028ec84f0fc06a5169d8afdde80))
* Fix ([`4cd7a83`](https://github.com/bdraco/index-503/commit/4cd7a8313e62d24cad563a5ec239712a93bc5cc4))
* Split ([`cff4d3b`](https://github.com/bdraco/index-503/commit/cff4d3b9fddc111d2be0b6d292916197153d647e))
* Split ([`b76c109`](https://github.com/bdraco/index-503/commit/b76c109cf8ba18064fd836330a5854e695905736))
* Fixup names ([`9d6eff7`](https://github.com/bdraco/index-503/commit/9d6eff7034ebfcbd2c18d94006897f4335ca5b86))
* Fixup names ([`1b5f55f`](https://github.com/bdraco/index-503/commit/1b5f55fba255ada17b42dc72a6d00eeb40591698))
* Fixup names ([`53c4ed6`](https://github.com/bdraco/index-503/commit/53c4ed62de2d1363fc1bd6d684a7cde7e8ef3f31))
* Fixup names ([`b8d26f9`](https://github.com/bdraco/index-503/commit/b8d26f9f5d4968af05485eceb04bd31f625d5c0f))
* Fixup names ([`c2d0137`](https://github.com/bdraco/index-503/commit/c2d0137793a14980fea264c7d3cb9d641af52c1c))
* Index ([`13ccf7b`](https://github.com/bdraco/index-503/commit/13ccf7b9a84b154ad35708dd0d468323a6e31391))
* Fix ([`c7e4cf7`](https://github.com/bdraco/index-503/commit/c7e4cf70e1986c5a99bcf07d75176ad7fb3e2fc5))
* Fix ([`a808dbc`](https://github.com/bdraco/index-503/commit/a808dbce2b77ce2363dc4592bfc33dace23efdbc))
* Fix ([`8b52162`](https://github.com/bdraco/index-503/commit/8b52162acf05ecc342e0a3ed865f5bbc0c63b002))
* Fix ([`0756c93`](https://github.com/bdraco/index-503/commit/0756c9393664492b320b74d1920f6e0eedbe2c07))
* Fix ([`e6bc8cc`](https://github.com/bdraco/index-503/commit/e6bc8ccb3214b4506d99d0886bc5dee36fe29cc7))
* Fix ([`cd30b99`](https://github.com/bdraco/index-503/commit/cd30b9929852552f42da5e3d0be8189dcb96ac29))
* Fix ([`42efaca`](https://github.com/bdraco/index-503/commit/42efacaae763c05304bba482f07745d68cdc888a))
* Fix ([`6cfcbf7`](https://github.com/bdraco/index-503/commit/6cfcbf7c18aa114596b77a1b200978f141c8d51e))
* Fix ([`f0faa81`](https://github.com/bdraco/index-503/commit/f0faa81355055ae927d472b1899dfda922dd73e1))
* Wip ([`7b3bca1`](https://github.com/bdraco/index-503/commit/7b3bca1e0652b21efaedaaa581ca03dbd4214e69))
* Wip ([`4235151`](https://github.com/bdraco/index-503/commit/4235151df36d737843d2761414249d2730709d85))
* Fixes ([`7d13b4a`](https://github.com/bdraco/index-503/commit/7d13b4a724333ca50aba24d9bf7770366f1a1149))
* Fixes ([`635e813`](https://github.com/bdraco/index-503/commit/635e813bbecc97998f3cb0de36d8d15895168860))
* Fixes ([`57fef5e`](https://github.com/bdraco/index-503/commit/57fef5e8352ed63edcd2980ac6e107adb6e7f002))
* Fixes ([`46a40be`](https://github.com/bdraco/index-503/commit/46a40bea8a1433fe62bf4d9c775830b0ca9a863c))
* Adjust ([`ce8f63e`](https://github.com/bdraco/index-503/commit/ce8f63e3ddc2573a09fde23099fecf108df13c86))
