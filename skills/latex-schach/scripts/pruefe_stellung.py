#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
pruefe_stellung.py – prüft Schachstellungen (FEN), bevor sie auf ein
Arbeitsblatt kommen. Braucht: pip install chess

  python3 pruefe_stellung.py "6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1"
  python3 pruefe_stellung.py --datei aufgaben.txt     # eine FEN pro Zeile
  python3 pruefe_stellung.py --matt 2 "FEN"           # Matt in 2 suchen

Ausgabe je Stellung: legal ja/nein, wer am Zug ist, Schach/Matt/Patt und
alle Mattzüge in N (Standard N=1) in englischer Notation – so, wie skak
sie in \\mainline erwartet. „Eindeutig" heißt: Es gibt genau einen
Lösungszug. Für Rätsel nur eindeutige Stellungen verwenden.
"""
import argparse
import sys

try:
    import chess
except ImportError:
    sys.exit("Bitte zuerst installieren: pip install chess")


def matt_in(board, n):
    """Liefert alle ersten Züge, die in höchstens n Zügen sicher mattsetzen."""
    loesungen = []
    for zug in board.legal_moves:
        board.push(zug)
        if erzwingt_matt(board, n - 1):
            loesungen.append(zug)
        board.pop()
    return loesungen


def erzwingt_matt(board, n):
    # board: Gegner am Zug, nachdem wir gezogen haben
    if board.is_checkmate():
        return True
    if n == 0 or board.is_game_over():
        return False
    for antwort in board.legal_moves:
        board.push(antwort)
        ok = any(_push_check(board, z, n) for z in list(board.legal_moves))
        board.pop()
        if not ok:
            return False
    return True


def _push_check(board, zug, n):
    board.push(zug)
    r = erzwingt_matt(board, n - 1)
    board.pop()
    return r


def pruefe(fen, n):
    try:
        b = chess.Board(fen)
    except ValueError as e:
        return f"FEHLER  {fen}\n        ungültige FEN: {e}"
    zeilen = [f"FEN     {fen}"]
    status = b.status()
    zeilen.append("legal   " + ("ja" if status == chess.STATUS_VALID else f"NEIN ({status!r})"))
    zeilen.append("am Zug  " + ("Weiß" if b.turn else "Schwarz"))
    if b.is_checkmate():
        zeilen.append("Lage    schon matt")
    elif b.is_stalemate():
        zeilen.append("Lage    patt")
    elif b.is_check():
        zeilen.append("Lage    Schach")
    if not b.is_game_over():
        l = matt_in(b, n)
        san = [b.san(z) for z in l]
        if l:
            zeilen.append(f"Matt in ≤{n}: {', '.join(san)}" + ("  (eindeutig)" if len(l) == 1 else "  (NICHT eindeutig)"))
        else:
            zeilen.append(f"Matt in ≤{n}: keins")
    return "\n".join(zeilen)


def main():
    p = argparse.ArgumentParser(description="Schachstellungen (FEN) prüfen")
    p.add_argument("fen", nargs="*")
    p.add_argument("--datei")
    p.add_argument("--matt", type=int, default=1, help="Matt in N suchen (Standard 1)")
    a = p.parse_args()
    fens = list(a.fen)
    if a.datei:
        with open(a.datei, encoding="utf-8") as f:
            fens += [z.strip() for z in f if z.strip() and not z.startswith("#")]
    if not fens:
        p.error("keine FEN angegeben")
    print("\n\n".join(pruefe(f, a.matt) for f in fens))


if __name__ == "__main__":
    main()
