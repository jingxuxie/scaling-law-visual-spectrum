# Validation report

## Static checks

- Main manuscript: 679 lines, 37 cited keys.
- Bibliography: 41 entries.
- Missing citation keys: none.
- New damping-knee script reruns successfully.

## New damping-knee results

| theta | rho | predicted knee | pre observed/predicted | post observed/predicted |
|---:|---:|---:|---:|---:|
| 1.00 | 1e-8 | 1.00e4 | 1.3332 / 1.3333 | 0.6685 / 0.6667 |
| 0.75 | 1e-6 | 1.00e5 | 1.0652 / 1.0667 | 0.6710 / 0.6667 |
| 0.50 | 1e-3 | 3.16e4 | 0.8817 / 0.8889 | 0.6763 / 0.6667 |

## Approximate page check

A local two-column syntax-check stub produced:

- 9 total pages including references;
- the `References` heading on page 8.

The official AAAI style file was not available in the execution environment, so
this is not a certification of the final page count. Compile with the official
`aaai2027.sty`; technical content must end by page 7.

## Remaining manual checks

1. Compile with the official AAAI-27 author kit.
2. Check figure legibility and float placement.
3. Resolve any overfull boxes reported by the official compile.
4. Verify that references begin no later than page 8.
5. Run the existing submission/anonymity checks.
