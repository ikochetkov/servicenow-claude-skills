---
name: mobiz-servicenow-pdf
description: Generate PDF reports server-side in ServiceNow using PDFGenerationAPI with inline SVG charts, CSS styling, tables, and images. Covers convertToPDF, convertToPDFWithHeaderFooter, CSS3 Paged Media, custom fonts, and the full pattern of HTML rendering + PDF attachment. Use whenever the user wants to generate a PDF, create a report with charts, attach a PDF to a record, convert HTML to PDF, build SVG gauge or bar charts for documents, automate scheduled reports with email attachments, or use iText7/PDFGenerationAPI in ServiceNow. Also use when the user asks about PDF limitations, print-color-adjust, or page break issues in ServiceNow.
---

# ServiceNow PDF Generation

Generate PDFs server-side in ServiceNow using `sn_pdfgeneratorutils.PDFGenerationAPI`. The API accepts an HTML string (with CSS and inline SVG) and creates a PDF attachment on any record.

**Plugin:** `com.snc.apppdfgenerator` (activated by default, Paris+)
**Namespace:** `sn_pdfgeneratorutils`
**Engine:** iText7 with CSS3 Paged Media support

## Quick Start

```javascript
var html = '<html><body><h1>Report</h1><p>Generated: ' + new GlideDateTime().getDisplayValue() + '</p></body></html>';
var pdfApi = new sn_pdfgeneratorutils.PDFGenerationAPI();
var result = pdfApi.convertToPDF(html, 'incident', incSysId, 'report.pdf');
// result: { status: 'success', attachment_id: '...', request_id: '...' }
```

## API Methods

### convertToPDF

```javascript
new sn_pdfgeneratorutils.PDFGenerationAPI().convertToPDF(
    html,           // String: complete HTML document
    targetTable,    // String: table to attach PDF to (e.g. 'u_temp', 'incident')
    targetSysId,    // String: sys_id of the record
    pdfName,        // String: filename (API appends .pdf automatically)
    fontSysId       // String (optional): sys_id from sys_pdf_generation_font_family
);
```

Returns object: `{ status: 'success'|'failure', attachment_id: '...', message: '...', request_id: '...' }`

**Filename gotcha:** The API auto-appends `.pdf` to `pdfName`. If you pass `'report.pdf'`, the attachment will be named `report.pdf.pdf`. Pass just `'report'` or strip the extension before calling.

### convertToPDFWithHeaderFooter

```javascript
var pageProps = {
    HeaderImageAttachmentId: '',       // sys_id of header image attachment
    HeaderImageAlignment: 'CENTER',    // 'LEFT', 'CENTER', 'RIGHT'
    PageSize: 'A4',                    // 'A4', 'LETTER', 'LEGAL'
    GeneratePageNumber: 'true',        // 'true' or 'false'
    TopOrBottomMargin: '72',           // points (72 = 1 inch)
    LeftOrRightMargin: '36'            // points (36 = 0.5 inch)
};

new sn_pdfgeneratorutils.PDFGenerationAPI().convertToPDFWithHeaderFooter(
    html,           // String: HTML content
    targetTable,    // String: table name
    targetSysId,    // String: record sys_id
    pdfName,        // String: filename
    pageProps,      // Object: page configuration
    fontSysId       // String (optional): font family sys_id
);
```

## SVG Charts in PDFs

The PDFGenerationAPI renders inline SVG natively. SVG is vector-based, so charts render at full quality in PDF without rasterization.

### Gauge Chart Pattern

```javascript
function buildGaugeSVG(actualHours, plannedHours) {
    var width = 320, height = 200, strokeWidth = 40;
    var cx = width / 2, cy = height - 30;
    var r = Math.min(width / 2 - strokeWidth / 2 - 10, height - strokeWidth / 2 - 20);
    var pct = plannedHours > 0 ? (actualHours / plannedHours) * 100 : 0;
    var basePct = Math.max(0, Math.min(100, pct));

    // Arc path helper
    function polarToCartesian(cx, cy, r, deg) {
        var rad = (deg * Math.PI) / 180;
        return { x: cx + r * Math.cos(rad), y: cy - r * Math.sin(rad) };
    }
    function describeArc(cx, cy, r, startDeg, endDeg) {
        var start = polarToCartesian(cx, cy, r, startDeg);
        var end = polarToCartesian(cx, cy, r, endDeg);
        var largeArc = Math.abs(endDeg - startDeg) > 180 ? 1 : 0;
        var sweep = startDeg > endDeg ? 1 : 0;
        return 'M ' + start.x + ' ' + start.y + ' A ' + r + ' ' + r + ' 0 ' + largeArc + ' ' + sweep + ' ' + end.x + ' ' + end.y;
    }

    var theta = 180 - (basePct / 100) * 180;
    var bgPath = describeArc(cx, cy, r, 180, 0);
    var valPath = basePct > 0 ? describeArc(cx, cy, r, 180, theta) : '';

    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + width + ' ' + height + '">'
        + '<path d="' + bgPath + '" fill="none" stroke="#E6E6E6" stroke-width="' + strokeWidth + '" />'
        + (valPath ? '<path d="' + valPath + '" fill="none" stroke="#4F7F2D" stroke-width="' + strokeWidth + '" />' : '')
        + '<text x="' + cx + '" y="' + (cy - strokeWidth * 0.3) + '" text-anchor="middle" font-size="36" font-weight="700">' + pct.toFixed(1) + '%</text>'
        + '</svg>';
}
```

### Bar Chart Pattern

```javascript
function buildBarChartSVG(labels, allocated, actual) {
    var width = 700, height = 300;
    var marginTop = 60, marginRight = 30, marginBottom = 60, marginLeft = 60;
    var chartWidth = width - marginLeft - marginRight;
    var chartHeight = height - marginTop - marginBottom;
    var maxVal = Math.max.apply(null, allocated.concat(actual).concat([1]));
    var yMax = Math.ceil(maxVal / 100) * 100 || 100;
    var groupWidth = chartWidth / labels.length;
    var barWidth = groupWidth * 0.35;
    var barGap = groupWidth * 0.05;
    var allocColor = '#1C1631', actualColor = '#4CAF50';

    // Y-axis ticks and grid lines
    var yAxisHtml = '';
    var yTicks = 5, yTickStep = yMax / yTicks;
    for (var t = 0; t <= yTicks; t++) {
        var val = t * yTickStep;
        var y = marginTop + chartHeight - (val / yMax) * chartHeight;
        yAxisHtml += '<line x1="' + marginLeft + '" y1="' + y + '" x2="' + (marginLeft + chartWidth) + '" y2="' + y + '" stroke="#e0e0e0" stroke-width="1" />';
        yAxisHtml += '<text x="' + (marginLeft - 8) + '" y="' + (y + 4) + '" text-anchor="end" font-size="10" fill="#666">' + Math.round(val) + '</text>';
    }

    // Bars with value labels and X-axis labels
    var barsHtml = '';
    for (var i = 0; i < labels.length; i++) {
        var groupX = marginLeft + i * groupWidth + groupWidth * 0.15;
        var allocH = (allocated[i] / yMax) * chartHeight;
        var actH = (actual[i] / yMax) * chartHeight;
        var actX = groupX + barWidth + barGap;

        barsHtml += '<rect x="' + groupX + '" y="' + (marginTop + chartHeight - allocH) + '" width="' + barWidth + '" height="' + allocH + '" fill="' + allocColor + '" />';
        barsHtml += '<text x="' + (groupX + barWidth / 2) + '" y="' + (marginTop + chartHeight - allocH - 5) + '" text-anchor="middle" font-size="9" font-weight="bold">' + (allocated[i] > 0 ? Math.round(allocated[i]) : '') + '</text>';

        barsHtml += '<rect x="' + actX + '" y="' + (marginTop + chartHeight - actH) + '" width="' + barWidth + '" height="' + actH + '" fill="' + actualColor + '" />';
        barsHtml += '<text x="' + (actX + barWidth / 2) + '" y="' + (marginTop + chartHeight - actH - 5) + '" text-anchor="middle" font-size="9" font-weight="bold">' + (actual[i] > 0 ? Math.round(actual[i]) : '') + '</text>';

        // X-axis label
        barsHtml += '<text x="' + (groupX + barWidth + barGap / 2) + '" y="' + (marginTop + chartHeight + 20) + '" text-anchor="middle" font-size="10">' + labels[i] + '</text>';
    }

    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + width + ' ' + height + '">'
        // Title
        + '<text x="' + (width / 2) + '" y="18" text-anchor="middle" font-size="14" font-weight="bold">Allocated vs Actual</text>'
        // Legend
        + '<rect x="' + (width / 2 - 90) + '" y="26" width="14" height="14" fill="' + allocColor + '" />'
        + '<text x="' + (width / 2 - 72) + '" y="37" font-size="11">Allocated</text>'
        + '<rect x="' + (width / 2 + 10) + '" y="26" width="14" height="14" fill="' + actualColor + '" />'
        + '<text x="' + (width / 2 + 28) + '" y="37" font-size="11">Actual</text>'
        // Axes
        + '<line x1="' + marginLeft + '" y1="' + marginTop + '" x2="' + marginLeft + '" y2="' + (marginTop + chartHeight) + '" stroke="#333" />'
        + '<line x1="' + marginLeft + '" y1="' + (marginTop + chartHeight) + '" x2="' + (marginLeft + chartWidth) + '" y2="' + (marginTop + chartHeight) + '" stroke="#333" />'
        + yAxisHtml + barsHtml
        + '</svg>';
}
```

## CSS Styling for PDFs

### Print-Safe CSS

```css
* {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
}
```

### Page Breaks

```css
.page-section:not(:first-of-type) { page-break-before: always; }
.no-break { page-break-inside: avoid; }
```

### CSS3 Paged Media (for headers/footers/page numbers)

```css
@page {
    size: A4 portrait;
    margin: 15mm;
    @bottom-right {
        font-family: sans-serif;
        font-size: 10px;
        content: "Page " counter(page) " of " counter(pages);
    }
    @top-center {
        content: element(runningHeader);
    }
}

#pageHeader {
    position: running(runningHeader);
}
```

### Table Styling That Works in PDFGenerationAPI

```css
table { width: 100%; border-collapse: collapse; font-size: 10px; }
th { background: #130E23; color: #fff; padding: 8px 6px; text-align: center; border: 1px solid #130E23; }
td { padding: 6px; border: 1px solid #ccc; text-align: center; }
tr.role-row { background: #F2F2F2; font-weight: bold; }
tr.grand-total { background: #130E23; color: #fff; font-weight: bold; }
```

## CSS Limitations in PDFGenerationAPI

| Feature | Works? | Workaround |
|---------|--------|------------|
| `background-color` | Yes | Use `print-color-adjust: exact` |
| `position: absolute` | No | Use spacer divs or flexbox |
| `display: flex` | Partial | Basic flex works, `margin-top: auto` does not |
| Inline SVG | Yes | Full support for paths, text, rect, circle |
| `@page` margins | Yes (Tokyo+) | Broken in San Diego, fixed in Tokyo |
| `page-break-before/after` | Yes | Standard CSS |
| Base64 images (`<img src="data:...">`) | Yes | Inline base64 PNG/SVG |
| External URLs in `<img>` | No | Must be base64 or publicly accessible |
| Custom fonts | Yes | Requires `sys_pdf_generation_font_family` record |

## Full Report Generation Pattern

### Script Include (Rhino JS — ES5 only)

```javascript
var MyReportRenderer = Class.create();
MyReportRenderer.prototype = {
    initialize: function() {
        this.logo = gs.getProperty('my_app.logo_base64') || '';
    },

    generateReportHtml: function(data) {
        var html = '<!DOCTYPE html><html><head><meta charset="UTF-8">';
        html += '<style>';
        html += '* { margin: 0; padding: 0; box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }';
        html += 'body { font-family: Helvetica, Arial, sans-serif; }';
        // ... add all CSS styles
        html += '</style></head><body>';

        // Cover page
        html += '<div class="cover">';
        html += '<img src="' + this.logo + '" />';
        html += '<h1>Report Title</h1>';
        html += '</div>';

        // Content pages with charts
        html += '<div class="section">';
        html += this._buildGaugeSVG(data.actual, data.planned);
        html += this._buildTable(data.rows);
        html += '</div>';

        html += '</body></html>';
        return html;
    },

    _buildGaugeSVG: function(actual, planned) {
        // ... SVG generation (see patterns above)
    },

    _buildTable: function(rows) {
        var html = '<table><thead><tr><th>Name</th><th>Value</th></tr></thead><tbody>';
        for (var i = 0; i < rows.length; i++) {
            html += '<tr><td>' + rows[i].name + '</td><td>' + rows[i].value + '</td></tr>';
        }
        html += '</tbody></table>';
        return html;
    },

    type: 'MyReportRenderer'
};
```

### Scheduled Job Pattern

```javascript
(function() {
    try {
        // 1. Query data
        var data = getReportData();

        // 2. Create temp record for attachment
        var temp = new GlideRecord('u_temp');
        temp.initialize();
        temp.setValue('u_type', 'my_report');
        var tempId = temp.insert();

        // 3. Generate HTML
        var renderer = new MyReportRenderer();
        var html = renderer.generateReportHtml(data);

        // 4. Convert to PDF (creates attachment automatically)
        var pdfApi = new sn_pdfgeneratorutils.PDFGenerationAPI();
        var result = pdfApi.convertToPDF(html, 'u_temp', tempId, 'My_Report.pdf');

        var resultObj = (typeof result === 'string') ? JSON.parse(result) : result;
        if (resultObj.status !== 'success') {
            gs.error('PDF generation failed: ' + JSON.stringify(resultObj));
            return;
        }

        // 5. Trigger notification with attachment
        gs.eventQueue('my_report_event', temp, tempId, 'My_Report.pdf');
        gs.info('Report generated successfully');

    } catch (ex) {
        gs.error('Report failed: ' + ex.message);
    }
})();
```

## Error Handling

The `convertToPDF` return value may be a string or an already-parsed object depending on context. Always handle both:

```javascript
var result = pdfApi.convertToPDF(html, table, sysId, name);
var resultObj = (typeof result === 'string') ? JSON.parse(result) : result;

if (!resultObj || resultObj.status !== 'success') {
    gs.error('PDF failed: ' + JSON.stringify(resultObj));
    // Common failure messages:
    //   "The Target table name - X is not valid" — table doesn't exist
    //   "Conversion failed" — HTML parsing error (check for malformed tags)
    //   null result — plugin not activated or API unavailable
}
```

After successful conversion, always verify the attachment was actually created:

```javascript
var att = new GlideRecord('sys_attachment');
att.addQuery('table_name', targetTable);
att.addQuery('table_sys_id', targetSysId);
att.addQuery('content_type', 'application/pdf');
att.orderByDesc('sys_created_on');
att.setLimit(1);
att.query();
if (!att.next()) {
    gs.error('PDF conversion reported success but no attachment found');
}
```

## HTML Size Considerations

The API handles large HTML strings well — tested with 155KB+ HTML producing 153KB PDFs with 27 pages of charts and tables. For very large reports:

- **System properties** have a practical limit around 4-8MB for storing base64 logos or HTML
- **String concatenation** in Rhino can be slow for very large strings — build HTML in sections
- **PDF output** is typically 60-80% smaller than the input HTML (vector compression)
- If generating reports with 50+ pages, consider splitting into multiple PDFs to avoid transaction timeouts

## Custom Fonts

1. Navigate to `sys_pdf_generation_font_family`
2. Create a new record with your font name
3. Attach `.ttf` font files to the record
4. Reference in CSS: `font-family: YourFontName;`
5. Pass the record's sys_id as the last parameter to `convertToPDF`

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Background colors missing | Print color adjust not set | Add `print-color-adjust: exact !important` to `*` selector |
| Page breaks not working | Wrong CSS property | Use `page-break-before: always` (not `break-before`) |
| SVG not rendering | Missing xmlns | Always include `xmlns="http://www.w3.org/2000/svg"` on `<svg>` tags |
| Fonts not applied | Missing font sys_id | Pass font family sys_id to convertToPDF |
| `@page` rules ignored | San Diego bug | Fixed in Tokyo+ — upgrade or use pageProperties parameter |
| Images not showing | External URL blocked | Convert images to base64 data URIs |
| `position: absolute` ignored | Not supported by iText7 | Use spacer divs, padding, or table layout |
| Result is `[object Object]` | Return value is already parsed | Use result directly, don't JSON.parse |
| Filename is `report.pdf.pdf` | API auto-appends `.pdf` | Pass `'report'` not `'report.pdf'` as pdfName |
| Transaction timeout on large reports | HTML too large / too many pages | Split into multiple PDFs or reduce page count |

## Reference Implementation

See `SanofiReportRenderer` Script Include — a production 43KB renderer that generates multi-page PDF reports with:
- Cover page with base64 logos
- Table of Contents
- Semi-circular gauge charts (SVG)
- Grouped bar charts (SVG)
- Stacked bar charts (SVG)
- Data tables with role/user hierarchy
- Context blocks with reporting periods
- Confidential footers

All rendered server-side using `PDFGenerationAPI.convertToPDF(html)` with zero external dependencies.
