# Porovnání kvality kódu generovaného pomocí různých velkých jazykových modelů v Pythonu

Repozitář s pomocnými soubory pro bakalářskou práci zaměřenou na porovnání kvality kódu generovaného pomocí vybraných velkých jazykových modelů v Pythonu. 

## Zadání

V současné době stále více vývojářů využívá generativní AI modely, jako jsou velké jazykové modely (LLM), pro zjednodušení a zefektivnění implementační části softwarového vývoje. S rostoucím využíváním těchto modelů se zvyšuje potřeba porozumět jejich schopnostem i omezením při generování kódu.

Cílem této bakalářské práce je komplexně zhodnotit a porovnat kvalitu kódu generovaného různými velkými jazykovými modely (LLM), konkrétně modely ChatGPT, Claude a Gemini, v programovacím jazyce Python. Práce se zaměří nejen na funkční správnost kódu, ale i na jeho mimofunkční vlastnosti, jako jsou efektivita a udržovatelnost. K hodnocení budou použity vhodné metriky a nástroje, například jednotkové testy pro ověření funkčnosti nebo lintery pro statickou analýzu kódu. Současně bude věnována pozornost různým technikám výzev (promptů) a jejich vlivu na kvalitu generovaného kódu. Klíčovou otázkou, kterou práce řeší, je, zda a jak se kvalita kódu mezi jednotlivými modely liší a který z těchto modelů je pro generování kvalitního kódu v jazyce Python nejvhodnější.

## Struktura repozitáře

    .
    ├── code                    # Adresář s vlastními skripty využitými v praktické části
    │   ├── convertor_to_csv    # Adresář s konvertorem výsledků testů do CSV formátu
    │   ├── scrapper            # Adresář se skriptem pro automatizované získávání výstupů
    │   └── tests               # Adresáře s testovacími skripty pro jednotlivé úlohy
    │       ├── ascii_art
    │       ├── calculator
    │       └── todo_list
    ├── generated               # Adresář s výstupy z velkých jazykových modelů
    │   ├── code                # Adresáře s extrahovaným Python kódem z výstupů
    │   │   ├── ascii_art
    │   │   ├── calculator
    │   │   └── todo_list
    │   └── results             # Adresáře s kompletními výstupy
    │       ├── ascii_art
    │       ├── calculator
    │       └── todo_list
    ├── prompts                 # Adresáře s výzvymi pro analyzované aplikace
    │   ├── ascii_art
    │   ├── calculator
    │   └── todo_list
    ├── results                 # Adresáře s výsledky měření kvality vygenerovaného kódu
    │   ├── ascii_art
    │   ├── calculator
    │   └── todo_list
    ├── thesis.pdf              # Text bakalářské práce v PDF
    ├── .gitignore
    └── README.md               