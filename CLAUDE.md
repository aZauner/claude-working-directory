# TUWEL Abgaben – Session-Anweisungen

## Ablauf bei jedem Run

1. Führe `/clear` aus, um den Chat zu leeren, bevor du beginnst.
2. Führe `tuwel_abgaben.py` aus (oder den inline-Skript-Block aus dem Prompt).
3. Präsentiere die Ergebnisse **ausschließlich als deutsche Aufzählungsliste** – keine Tabellen, keine englischen Texte.
4. Sende danach eine Push-Benachrichtigung (PushNotification-Tool) mit einer Zusammenfassung der Abgaben.

## Ausgabeformat

Wenn Abgaben gefunden wurden, gib sie so aus:

```
TUWEL Abgaben – nächste 14 Tage:

• <Titel> – <Kurs> – <Datum> MESZ (in <Zeit>)
• ...
```

Wenn keine Abgaben vorhanden sind:

```
Keine Abgaben in den nächsten 14 Tagen.
```

Verwende **keine Markdown-Tabellen** in der Antwort. Nur Aufzählungszeichen (`•`).

## Push-Benachrichtigung

Sende nach der Ausgabe immer eine Benachrichtigung mit dem PushNotification-Tool.

- Wenn Abgaben vorhanden: Liste die nächste(n) Deadline(n) knapp auf (Titel + Datum).
- Wenn keine: Sende keine Benachrichtigung (kein Spam bei leerem Ergebnis).
