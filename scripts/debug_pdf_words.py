import fitz

pdf = fitz.open("data/pdfs/s_TM100B25.pdf")

page = pdf[0]

words = page.get_text("words")

words.sort(key=lambda w: (round(w[1]), w[0]))

for w in words:
    x0, y0, x1, y1, text, *_ = w

    if 120 < y0 < 140:

        print(
            f"{y0:7.1f} "
            f"{x0:7.1f} "
            f"{text}"
        )