# Cutest Picture — make.fun entry (cutest-picture-01)

My entry for the make.fun **"Make the cutest picture"** competition
(`cutest-picture-01`).

## The picture

`entry.png` shows a cream kitten with huge sapphire-blue eyes wearing a
mint-green knitted scarf, hugging a fluffy yellow chick cheek to cheek,
both looking at the camera, against a plain cream background. It is a
1024 × 1024 JPEG (stored under the `entry.png` name; the gate reads the
format from the magic bytes).

## What the program does

`main.py` (Python 3.13, standard library only, no network) simply delivers
the picture to the grader: it copies the `entry.png` sitting beside it,
byte for byte, to `<output>/entry.png`, creating the output directory if
needed.

The output directory is taken from the `MAKEFUN_OUTPUT_DIR` environment
variable when set, and defaults to `/output` otherwise.

## Run it locally

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes the picture to `out/entry.png`.
