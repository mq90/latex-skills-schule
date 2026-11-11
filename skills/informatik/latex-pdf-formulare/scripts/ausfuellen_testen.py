#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Simuliert eine Schülerin, die das Formular in Chrome/Edge (PDFium) ausfüllt:
klickt in Felder, tippt Text, klickt Kästchen an, speichert und rendert.
Aufruf: python3 ausfuellen_testen.py ein.pdf aus.pdf antworten.json bild_praefix
antworten.json: {"feldname": "Text", "kaestchen": true, "optionsfeld": 1 (Index des Knopfes)}
Benötigt: pip install pypdfium2 pymupdf"""
import json, sys, ctypes
import pymupdf, pypdfium2 as pdfium, pypdfium2.raw as raw

ein, aus, antw, bild = sys.argv[1:5]
antworten = json.load(open(antw, encoding="utf-8"))

# Feldpositionen aus PyMuPDF (Ursprung oben links) holen
mu = pymupdf.open(ein)
ziele = []  # (seite, x, y_pdf, name, typ, wert)
for sn, page in enumerate(mu):
    h = page.rect.height
    for w in page.widgets():
        if w.field_name in antworten:
            wert = antworten[w.field_name]
            if w.field_type == pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON:
                # bei Radio: nur das Widget mit passender Beschriftung (Index) anklicken
                pass
            r = w.rect
            ziele.append((sn, (r.x0 + r.x1) / 2, h - (r.y0 + r.y1) / 2, w.field_name, w.field_type_string, wert, r))

pdf = pdfium.PdfDocument(ein)
form = pdf.init_forms()
handle = pdf.formenv.raw
for sn in range(len(pdf)):
    page = pdf[sn]
    raw.FORM_OnAfterLoadPage(page.raw, handle)
    for (s, x, y, name, typ, wert, r) in ziele:
        if s != sn:
            continue
        if typ == "RadioButton":
            continue
        raw.FORM_OnMouseMove(handle, page.raw, 0, x, y)
        if typ == "CheckBox":
            if wert:
                raw.FORM_OnLButtonDown(handle, page.raw, 0, x, y)
                raw.FORM_OnLButtonUp(handle, page.raw, 0, x, y)
                raw.FORM_ForceToKillFocus(handle)
            continue
        # Textfeld: hineinklicken, tippen
        raw.FORM_OnLButtonDown(handle, page.raw, 0, x, y)
        raw.FORM_OnLButtonUp(handle, page.raw, 0, x, y)
        for ch in wert:
            if ch == "\n":
                raw.FORM_OnKeyDown(handle, page.raw, 0x0D, 0); raw.FORM_OnChar(handle, page.raw, 0x0D, 0); raw.FORM_OnKeyUp(handle, page.raw, 0x0D, 0)
            else:
                raw.FORM_OnChar(handle, page.raw, ord(ch), 0)
        raw.FORM_ForceToKillFocus(handle)
    # Radiobuttons: Wert ist der Index des anzuklickenden Knopfes
    for name in {z[3] for z in ziele if z[4] == "RadioButton" and z[0] == sn}:
        knoepfe = [z for z in ziele if z[3] == name and z[0] == sn]
        knoepfe.sort(key=lambda z: (-(z[2]), z[1]))
        z = knoepfe[antworten[name]]
        raw.FORM_OnLButtonDown(handle, page.raw, 0, z[1], z[2])
        raw.FORM_OnLButtonUp(handle, page.raw, 0, z[1], z[2])
        raw.FORM_ForceToKillFocus(handle)
    raw.FORM_OnBeforeClosePage(page.raw, handle)

pdf.save(aus)
# so, wie Chrome die gespeicherte Datei wieder anzeigt
neu = pdfium.PdfDocument(aus)
neu.init_forms()
for sn in range(len(neu)):
    neu[sn].render(scale=1.4, may_draw_forms=True).to_pil().save(f"{bild}-{sn+1}.png")
