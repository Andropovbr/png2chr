# png2chr

Uma ferramenta simples em Python para converter sprite sheets em PNG para o formato CHR utilizado pelo Nintendo Entertainment System (NES).

O objetivo deste projeto é facilitar o desenvolvimento homebrew para NES no Linux, oferecendo uma alternativa simples e extensível para conversão de gráficos.

> **Status:** Em desenvolvimento 🚧

---

## Funcionalidades atuais

- Leitura de imagens PNG
- Conversão para arquivos `.chr`
- Geração de tiles no formato nativo do NES
- Validação de largura e altura (múltiplos de 8)
- Suporte a transparência
- Análise de cores por tile
- Modo de análise antes da conversão
- Geração de imagens de debug para localizar tiles problemáticos
- Suporte opcional a paleta global
- Substituição de cores durante a conversão (`--replace`)

---

## Requisitos

- Python 3
- Pillow

Instalação:

```bash
pip install pillow
```

---

## Estrutura do projeto

```
png2chr/
├── png2chr.py
├── analyzer.py
├── chr_writer.py
├── debug_tools.py
├── image_tools.py
└── palette_tools.py
```

---

## Como analisar uma imagem

Antes de converter, recomenda-se executar uma análise:

```bash
python3 png2chr.py analyze player.png
```

A ferramenta informa:

- tamanho da imagem
- quantidade de tiles
- cores encontradas
- paleta sugerida
- tiles problemáticos

Caso existam problemas, é gerado um mapa destacando os tiles que precisam de atenção.

---

## Converter para CHR

Conversão simples:

```bash
python3 png2chr.py convert player.png player.chr
```

Se a imagem possuir apenas quatro cores, uma paleta global será criada automaticamente.

---

## Usando uma paleta fixa

Também é possível informar explicitamente a paleta:

```bash
python3 png2chr.py convert player.png player.chr \
    --palette "0,0,0,0;0,0,0,255;248,56,0,255;252,224,168,255"
```

---

## Substituindo cores

Caso seja necessário adaptar um sprite ao limite de cores do NES:

```bash
python3 png2chr.py convert player.png player.chr \
    --replace "63,63,116,255=0,0,0,255"
```

É possível utilizar várias opções `--replace`.

---

## Debug

Durante a análise ou conversão:

```bash
python3 png2chr.py analyze player.png --debug
```

A ferramenta gera:

- imagem ampliada do tile problemático;
- mapa indicando todos os tiles com problemas.

Esses arquivos auxiliam na correção da arte antes da geração do CHR.

---

## Formato CHR

Cada tile possui 8×8 pixels.

Cada tile é convertido para 16 bytes:

```
8 bytes -> bitplane 0
8 bytes -> bitplane 1
```

Compatível com o formato utilizado pelo NES.

---

## Roadmap

Funcionalidades planejadas:

- [ ] Remover tiles duplicados
- [ ] Preview do CHR gerado
- [ ] Exportar índice dos tiles
- [ ] Gerar arquivo `.asm` automaticamente
- [ ] Crop da sprite sheet
- [ ] Múltiplas paletas de sprite
- [ ] Interface gráfica
- [ ] Exportação de metadados para uso em jogos

---

## Motivação

Existem diversas ferramentas para manipulação de CHR, porém muitas são antigas, dependem de Wine ou possuem fluxo de uso pouco amigável.

Este projeto nasceu durante o desenvolvimento de um jogo para NES em Assembly 6502 utilizando **ca65/ld65**, com o objetivo de simplificar a conversão de sprite sheets em PNG para o formato CHR.

---

## Licença

MIT