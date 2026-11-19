# The Alphabet — reader

A fixed list of words, and a rule for reading any Bitcoin block hash through it. The list was locked and its hash carved on Bitcoin before any reading was published.

Open the reader: [reader.html](reader.html)

## The list

[`alphabet.txt`](alphabet.txt) holds 8 columns of 256 words each, 2,048 words in all. Each column starts with a header line (`# column N: name`), followed by its words in index order, from 0 to 255. Index 0 is `quiet` in every column.

SHA-256 of `alphabet.txt`:

```
7483a0908ea1ae4553aa7808fceb6b414433064493bff353dca19ac73cb4b957
```

## The carving

| | |
|---|---|
| Block height | 976,509 |
| Txid | [`224fccf84fbdbf5435f35efdcd0c8c1a5a4694612fb8f7121c8b56a6f8c1614e`](https://mempool.space/tx/224fccf84fbdbf5435f35efdcd0c8c1a5a4694612fb8f7121c8b56a6f8c1614e) |
| Script | OP_RETURN, `6a20` + the 32-byte hash above |

The full record and the proof readings are in [CARVING.md](CARVING.md).

## The reading rule

1. Take the block hash as 64 hexadecimal characters, in the usual display order.
2. **Silence.** Count the leading `0` hex characters. That count is the Silence, read as that many `quiet` words.
3. **Words.** Take the next 16 hex characters after the Silence as 8 bytes, two characters each. Byte 1 indexes column 1, byte 2 indexes column 2, and so on up to column 8.
4. The word at that index in that column is the reading. The first word is the **Sign**.

The columns are: 1 subject, 2 verb, 3 object or connective, 4 place, 5 connective or verb, 6 subject, 7 verb, 8 final word.

- The first character after the Silence is never `0`, so byte 1 is always 16 or more. Column 1's indices 1–15 can never be read.
- A zero byte in positions 2–8 reads as `quiet` in that column.

### Example: block 0

Hash: `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`

- Silence: 10 characters, so the reading opens with 10 `quiet`s.
- Bytes: `19 d6 68 9c 08 5a e1 65`, which is 25 214 104 156 8 90 225 101.
- Reading: **diver welcomed skull vineyard where fishwife sang ancient**. The Sign is *diver*.

## Verify it yourself

```bash
sha256sum alphabet.txt
```

```bash
python3 reader8.py 976509
```

```bash
python3 read_layer.py 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
```

The first must print the hash above, and that hash must match the OP_RETURN of the carving transaction. `reader8.py` fetches the block hash from mempool.space; `read_layer.py` needs no network. Any block gives the same words for everyone.

## Files

| File | What it is |
|---|---|
| [`reader.html`](reader.html) | The reader page. Type a block height, see the Silence, the eight words and the Sign. |
| [`alphabet.txt`](alphabet.txt) | The carved list |
| [`CARVING.md`](CARVING.md) | The on-chain record of the carving, with the proof readings |
| [`glosses.txt`](glosses.txt) | One plain English gloss per word. Not carved, and not part of the reading rule. |
| `gloss_src/`, [`make_glosses.py`](make_glosses.py) | The gloss sources and the script that builds `glosses.txt` |
| [`reader.template.html`](reader.template.html), [`build.py`](build.py) | The page source and the script that bakes the list and glosses into `reader.html`. It refuses to build if the list does not match the carved hash or the proof readings. |
| [`reader8.py`](reader8.py) | Reads a block by height |
| [`read_layer.py`](read_layer.py) | Reads a block hash with no network access |
| [`columns8.py`](columns8.py) | The same eight columns as Python lists |
| `reader.py`, `score.py`, `score8.py`, `lexicon.py`, `tags8.json`, `sets8.json` | Needed by `reader8.py`. The score is an editorial tool for finding readings worth showing. It is not part of the reading rule and is not carved. |
| `proof-*.png`, `gloss-976609.png` | Screenshots of the reader on the proof blocks |

## Authorship and license

The Alphabet was authored by the owner of this repository. Its hash was carved on Bitcoin at block 976,509, in the transaction above. Any copy or fork must keep this attribution and the carving txid.

The word list, the glosses and the reader page are under Creative Commons Attribution 4.0. The Python scripts are under the MIT license. See [LICENSE](LICENSE).
