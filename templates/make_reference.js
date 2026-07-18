// Generates templates/reference.docx — the Pandoc style template.
// Run with: node templates/make_reference.js
//
// Why this script exists:
//   reference.docx is a binary file. Committing it to git means nobody can
//   see what changed or why. This script is the source of truth — it documents
//   every style decision and can regenerate the file from scratch on any machine.
//
// Requirements:
//   npm install docx jszip   (in the templates/ folder, or project root)

const { Document, Packer, Paragraph, TextRun, AlignmentType } = require("docx");
const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");

// ── Constants ────────────────────────────────────────────────────────────────

const TNR = "Times New Roman";
const COURIER = "Courier New";

// 1.25 cm in DXA (twips). 1 cm = 567 DXA.
const FIRST_LINE_INDENT = 709;

// Line spacing presets. Base unit is 240 twips = single spacing.
// Multiply 240 by the desired factor to get the value.
const SPACING_SINGLE = { line: 240, lineRule: "auto" };
const SPACING_115 = { line: 276, lineRule: "auto" }; // 240 * 1.15
const SPACING_15 = { line: 360, lineRule: "auto" }; // 240 * 1.5

// ── Document ─────────────────────────────────────────────────────────────────

var doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: TNR, size: 28, color: "000000" }, // 14pt = 28 half-points
        paragraph: { spacing: SPACING_15, alignment: AlignmentType.JUSTIFIED },
      },
    },

    paragraphStyles: [
      // ── Body text ──────────────────────────────────────────────────────────
      // Used for normal paragraphs from markdown
      {
        id: "Normal",
        name: "Normal",
        run: { font: TNR, size: 28 },
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 0, after: 0 },
          indent: { firstLine: FIRST_LINE_INDENT },
          alignment: AlignmentType.JUSTIFIED,
        },
      },

      // ── Headings ───────────────────────────────────────────────────────────
      // # maps to Heading 1, ## to Heading 2, ### to Heading 3
      // University format: same size as body, just bold — no font size increase
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: {
          font: TNR,
          size: 28,
          bold: true,
          color: "000000",
          allCaps: true,
        },
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 240, after: 120 },
          indent: { firstLine: 0 },
          alignment: AlignmentType.CENTER,
          outlineLevel: 0, // required for TOC detection
        },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: TNR, size: 28, bold: true, color: "000000" },
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 160, after: 80 },
          indent: { firstLine: 709 },
          alignment: AlignmentType.LEFT,
          outlineLevel: 1,
        },
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: {
          font: TNR,
          size: 28,
          bold: true,
          italics: true,
          color: "000000",
        },
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 120, after: 60 },
          indent: { firstLine: 709 },
          alignment: AlignmentType.LEFT,
          outlineLevel: 2,
        },
      },

      // ── Code blocks ────────────────────────────────────────────────────────
      // IMPORTANT: Pandoc looks for exactly "Source Code" — not "Code".
      // If the name doesn't match, Pandoc silently falls back to Normal.
      {
        id: "SourceCode",
        name: "Source Code",
        basedOn: "Normal",
        run: { font: COURIER, size: 20, color: "000000" }, // 10pt
        paragraph: {
          spacing: { line: 240, lineRule: "auto", before: 60, after: 60 },
          indent: { left: 709, firstLine: 0 }, // indent block, no first-line
          alignment: AlignmentType.LEFT,
        },
      },

      // ── Table cell text ────────────────────────────────────────────────────
      // IMPORTANT: Pandoc uses "Compact" for text inside table cells — not "Normal".
      // Before/after 0 keeps rows tight. 1.15 spacing matches Word default table feel.
      {
        id: "Compact",
        name: "Compact",
        basedOn: "Normal",
        run: { font: TNR, size: 28, color: "000000" },
        paragraph: {
          spacing: { line: 276, lineRule: "auto", before: 0, after: 0 },
          indent: { firstLine: 0 },
          alignment: AlignmentType.LEFT,
        },
      },

      // ── Figure captions ────────────────────────────────────────────────────
      // Used for "Рисунок – ..." lines below images
      {
        id: "ImageCaption",
        name: "Image Caption",
        basedOn: "Normal",
        run: { font: "Times New Roman", size: 28, color: "000000" },
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 0, after: 240 },
          indent: { firstLine: 0 },
          alignment: AlignmentType.CENTER,
        },
      },

      // Pandoc uses "Figure" for standalone image paragraphs
      {
        id: "Figure",
        name: "Figure",
        basedOn: "Normal",
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 0, after: 0 },
          indent: { firstLine: 0 },
          alignment: AlignmentType.CENTER,
        },
      },

      // Pandoc uses "Captioned Figure" when image has alt text in ![]()
      // This is the style applied to the image paragraph itself
      {
        id: "CaptionedFigure",
        name: "Captioned Figure",
        basedOn: "Normal",
        paragraph: {
          spacing: { line: 360, lineRule: "auto", before: 0, after: 0 },
          indent: { firstLine: 0 },
          alignment: AlignmentType.CENTER,
        },
      },

      // ── First paragraph after heading ──────────────────────────────────────
      // Pandoc applies this to the first paragraph after a heading — no indent
      {
        id: "FirstParagraph",
        name: "First Paragraph",
        basedOn: "Normal",
        paragraph: { indent: { firstLine: 709 } },
      },

      // Page break style — used via ::: {custom-style="pagebreak"} ::: in Markdown
      {
        id: "pagebreak",
        name: "pagebreak",
        basedOn: "Normal",
        paragraph: {
          spacing: { line: 240, lineRule: "auto", before: 0, after: 0 },
          indent: { firstLine: 0 },
          pageBreakBefore: true, // this is the key property
        },
      },
    ],
  },

  // ── Page layout ─────────────────────────────────────────────────────────
  // A4: 21.0cm x 29.7cm. Converting cm to DXA: 1cm = 567 DXA.
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }, // 2cm all sides
        },
      },
      children: [
        new Paragraph({
          children: [
            new TextRun({
              text: "Этот файл является шаблоном стилей. Не редактируйте содержимое.",
              font: TNR,
              size: 24,
              italics: true,
              color: "888888",
            }),
          ],
        }),
      ],
    },
  ],
});

// ── Inject Table style as raw XML ────────────────────────────────────────────
//
// WHY raw XML: The docx library only supports w:type="paragraph" styles.
// Table styles use w:type="table" which the library doesn't expose.
// Solution: let the library generate the file, then open the zip,
// patch styles.xml as a string, and repack.
//
// w:tblBorders defines borders for the whole table.
// insideH = internal horizontal lines (between rows)
// insideV = internal vertical lines (between columns)
// w:sz="4" = 0.5pt border thickness (sz is in eighths of a point)
//
// IMPORTANT: In a w:style of type="table", paragraph and run defaults
// MUST be placed inside <w:tblStylePr w:type="wholeTable">, NOT as bare
// <w:pPr>/<w:rPr> children of <w:style>. Bare pPr/rPr at the style level
// are valid only for paragraph styles — in a table style they violate the
// OOXML schema and Word/LibreOffice may ignore or misapply the formatting.
// Use w:tblStylePr to correctly cascade font and spacing into all cells.

var tableStyleXml = [
  '<w:style w:type="table" w:customStyle="1" w:styleId="Table">',
  '  <w:name w:val="Table"/>',
  "  <w:tblPr>",
  "    <w:tblBorders>",
  '      <w:top     w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  '      <w:left    w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  '      <w:bottom  w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  '      <w:right   w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  '      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  '      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>',
  "    </w:tblBorders>",
  "    <w:tblCellMar>",
  '      <w:top    w:w="60"  w:type="dxa"/>',
  '      <w:left   w:w="108" w:type="dxa"/>',
  '      <w:bottom w:w="60"  w:type="dxa"/>',
  '      <w:right  w:w="108" w:type="dxa"/>',
  "    </w:tblCellMar>",
  "  </w:tblPr>",
  '  <w:tblStylePr w:type="wholeTable">',
  "    <w:pPr>",
  '      <w:spacing w:before="0" w:after="0" w:line="276" w:lineRule="auto"/>',
  '      <w:ind w:firstLine="0"/>',
  "    </w:pPr>",
  "    <w:rPr>",
  '      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>',
  '      <w:sz w:val="24"/>',
  '      <w:szCs w:val="24"/>',
  "    </w:rPr>",
  "  </w:tblStylePr>",
  "</w:style>",
].join("\n");

Packer.toBuffer(doc)
  .then(function (buffer) {
    return JSZip.loadAsync(buffer).then(function (zip) {
      return zip
        .file("word/styles.xml")
        .async("string")
        .then(function (stylesXml) {
          stylesXml = stylesXml.replace(
            "</w:styles>",
            tableStyleXml + "\n</w:styles>",
          );
          zip.file("word/styles.xml", stylesXml);

          return zip.generateAsync({
            type: "nodebuffer",
            compression: "DEFLATE",
          });
        });
    });
  })
  .then(function (finalBuffer) {
    // Output path: same directory as this script
    var outPath = path.join(__dirname, "reference.docx");
    fs.writeFileSync(outPath, finalBuffer);
    console.log("Generated: " + outPath);
  })
  .catch(function (err) {
    console.error("Error:", err);
    process.exit(1);
  });
