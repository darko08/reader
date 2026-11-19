# The Alphabet — carving record

The Alphabet was locked and its hash carved on Bitcoin before any reading was published.

| | |
|---|---|
| File | `alphabet.txt` (8 columns × 256 words = 2,048 words, 2,056 lines with headers) |
| SHA-256 | `7483a0908ea1ae4553aa7808fceb6b414433064493bff353dca19ac73cb4b957` |
| Carved in | OP_RETURN, output 0, 0 sats |
| Script | `6a20` + the 32-byte hash (OP_RETURN, push 32 bytes, nothing else) |
| Txid | [`224fccf84fbdbf5435f35efdcd0c8c1a5a4694612fb8f7121c8b56a6f8c1614e`](https://mempool.space/tx/224fccf84fbdbf5435f35efdcd0c8c1a5a4694612fb8f7121c8b56a6f8c1614e) |
| Block height | 976,509 |
| Block hash | `000000000000000000012dd0da669d631c949621728a2feec24a039be0ebfc3b` |
| Fee | 459 sats (153 vB at 3 sat/vB) |

## The reading rule

1. Take the block hash as 64 hex characters.
2. Count the leading `0` hex characters. That is the **Silence**, read as that many `quiet`s.
3. Read the next 16 hex characters as 8 bytes, one per column, mod 256.
4. Each byte is an index into its column. The first word is the **Sign**.

| Column | Role |
|---|---|
| 1 | subject (indices 1–15 can never be read) |
| 2 | verb |
| 3 | object or connective |
| 4 | place |
| 5 | connective or verb (179 connectives, 76 verbs) |
| 6 | subject (people, creatures, weather; no overlap with column 1) |
| 7 | verb |
| 8 | final word |

Index 0 is `quiet` in every column. Every column holds 256 distinct words.

## Anchor readings

| Block | Silence | Reading | Sign |
|---|---|---|---|
| 0 (genesis) | 10 | diver welcomed skull vineyard where fishwife sang ancient | diver |
| 689,301 | 19 | oath trusted vow gallery hide gale punished shorn | oath |
| 976,500 | 19 | tender sobbed one gate or narwhal meant gentle | tender |
| 976,509 (the carving block) | 19 | i bore under cistern may peace murmured seaward | i |
| 976,609 (the block where the first layer claim landed) | 20 | cradle stirred drowned village could thunder came ancient | cradle |

## Verify it yourself

```bash
sha256sum alphabet.txt
```

```bash
python3 reader8.py 976509
```

The hash must match the table above, and so must the OP_RETURN of the transaction linked above. Any block read with `reader8.py` gives the same words for everyone.

## What this proves, and what it does not

- **Proves:** the word list was fixed at block 976,509. Every reading after that comes from the chain, not from the author.
- **Does not prove:** that the chain "means" anything. The list is the author.

## Domain

The reader is served at `readthestone.com`.

| | |
|---|---|
| Domain | `readthestone.com` |
| Recorded at block height | 976,619 |
| Block hash | `00000000000000000001cd9de0c31532e3e9f79092e6df248eddcbe82ce64ad7` |
| That block's reading | tenth commanded fear room only castaway howled half (Silence 19, Sign *tenth*) |

The height is the chain tip at the moment the domain was set for this site, on 19 November 2026 (UTC). It is a note in this file, not an on-chain record.
