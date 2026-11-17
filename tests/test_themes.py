"""Offline checks for palette completeness and Orca's runtime contrast gates."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ANSI = 'black red green yellow blue magenta cyan white brightBlack brightRed brightGreen brightYellow brightBlue brightMagenta brightCyan brightWhite'.split()


def read(path):
    return json.loads((ROOT / path).read_text())


def luminance(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return sum(weight * (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
               for weight, v in zip((0.2126, 0.7152, 0.0722), rgb))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


class ThemeTests(unittest.TestCase):
    def test_contrast_calculation(self):
        self.assertAlmostEqual(contrast('#000000', '#FFFFFF'), 21)
        self.assertEqual(contrast('#123456', '#123456'), 1)

    def test_variants(self):
        manifest = read('orca-plugin.json')
        self.assertEqual(manifest['execution'], 'data')
        self.assertEqual(manifest['capabilities'], [])
        for kind in ('themes', 'terminalThemes'):
            self.assertEqual([entry['id'] for entry in manifest['contributes'][kind]],
                             ['kanagawa-wave', 'kanagawa-dragon', 'kanagawa-lotus'])
        for variant, bg, fg in [('wave', '#1F1F28', '#DCD7BA'),
                                ('dragon', '#181616', '#C5C9C5'),
                                ('lotus', '#F2ECBC', '#545464')]:
            with self.subTest(variant=variant):
                app = read(f'themes/{variant}.json')
                terminal = read(f'terminal/{variant}.json')
                mode = 'light' if variant == 'lotus' else 'dark'
                self.assertEqual(app['base'], mode)
                self.assertEqual(terminal['mode'], mode)
                t = app['tokens']
                self.assertEqual(t['--background'], bg)
                self.assertEqual(t['--foreground'], fg)
                palette = terminal['terminal']
                self.assertEqual(palette['background'], bg)
                self.assertEqual(palette['foreground'], fg)
                self.assertTrue(set(ANSI + ['cursor', 'selectionBackground']) <= palette.keys())
                for color in list(t.values()) + list(palette.values()):
                    self.assertRegex(color, r'^#[0-9A-Fa-f]{6}$')
                for surface, text in [('background', 'foreground'), ('editor-surface', 'foreground'),
                                      ('card', 'card-foreground'), ('popover', 'popover-foreground'),
                                      ('primary', 'primary-foreground'), ('secondary', 'secondary-foreground'),
                                      ('muted', 'muted-foreground'), ('accent', 'accent-foreground'),
                                      ('sidebar', 'sidebar-foreground'), ('sidebar-accent', 'sidebar-accent-foreground'),
                                      ('tab-active', 'tab-active-foreground'), ('tab-inactive', 'tab-inactive-foreground'),
                                      ('worktree-sidebar-active', 'sidebar-foreground'),
                                      ('chat-user-message', 'foreground'), ('chat-user-message', 'chat-bold-foreground'),
                                      ('background', 'chat-muted-foreground'), ('chat-code-block', 'chat-muted-foreground'),
                                      ('chat-inline-code', 'chat-inline-code-foreground'), ('chat-inline-code', 'text-link'),
                                      ('editor-surface', 'text-link')]:
                    self.assertGreaterEqual(contrast(t['--' + surface], t['--' + text]), 4.5,
                                            f'{variant}: {surface}/{text}')
                for key, color in t.items():
                    if key.startswith('--git-decoration-'):
                        self.assertGreaterEqual(contrast(color, t['--sidebar']), 3, f'{variant}: {key}')
                for rule in app['tokenColors']:
                    self.assertTrue(rule['scope'])
                    for scope in rule['scope']:
                        self.assertRegex(scope, r'^[\w.-]+$')
                    color = rule['settings'].get('foreground')
                    if color:
                        self.assertGreaterEqual(contrast(color, bg), 3, f'{variant}: {rule["scope"]}')
                self.assertGreaterEqual(contrast(fg, palette['selectionBackground']), 4.5)
        for kind in ('themes', 'terminalThemes'):
            for entry in manifest['contributes'][kind]:
                self.assertLessEqual((ROOT / entry['path']).stat().st_size, 16 * 1024)


if __name__ == '__main__':
    unittest.main()
