# Textová hra Dungeon v Pythonu

Textový rogue-like dungeon crawler vytvořený jako zápočtový projekt do předmětu Úvod do Pythonu. Hráč prochází náhodně generovaným bludištěm, bojuje s monstry a vylepšuje své statistiky.

## Hlavní funkce
* **Náhodné generování mapy**: Bludiště je dynamicky vytvářeno pomocí randomizovaného algoritmu prohledávání do hloubky (DFS).
* **Tahový pohyb a boj**: Možnost chodit do všech čtyř stran a tahový soubojový systém inspirovaný hody kostkou (d20 pro šanci na zásah, d6 pro poškození).
* **Pokročilá UI nepřátel**: Příšera **Beholder** detekuje hrdinu na vzdálenost 10 políček (Manhattanská metrika) a k inteligentnímu pronásledování a obcházení zdí využívá algoritmus prohledávání do šířky (BFS).
* **Přehledový panel (HUD)**: Vykreslování aktuálního stavu hrdiny (HP, zlaťáky, stamina, XP a úroveň) v reálném čase přímo nad mapou dungeonu.
* **Ukládání a nahrávání**: Stav hry lze kdykoliv bezpečně uložit do souboru a později načíst díky implementaci modulu `pickle`.

## Jak hrát
1. Spusť hru lokálně pomocí Pythonu 3:
   ```bash
   python main.py
   ```
2. Zadej jméno svého hrdiny nebo načti již existující uloženou pozici ze souboru.
3. **Ovládání**: 
   * `U`, `D`, `L`, `R` pro pohyb (Nahoru, Dolů, Doleva, Doprava).
   * `A` pro útok na nepřátele (Attack).
   * `S` pro uložení rozehrané hry (Save).
   * `Q` pro ukončení hry (Quit).

## Struktura souborů
* `main.py` - Vstupní bod hry, řeší hlavní herní smyčku, uživatelský vstup a logiku ukládání a načítání.
* `dungeon.py` - Obsahuje třídu `Dungeon`, která se stará o generování mapy, umisťování entit, pohyb a boj.
* `map_entities.py` - Definuje chování a statistiky postav: `Hero`, `Goblin` a inteligentního nepřítele `Beholder`.
* `abstract_classes.py` - Poskytuje abstraktní třídy (`AbstractDungeon` a `Creature`), které definují celkovou architekturu hry.