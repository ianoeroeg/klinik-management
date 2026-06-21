# ♿ Accessibility (A11y) - Klinik Management System

Dokumén ieu ngajelaskeun standar accessibility pikeun Klinik Management System, dumasar kana **WCAG 2.1 Level AA**.

---

## 📋 Daptar Fitur Accessibility

### ✅ 1. Semantic HTML
- Ngagunakeun tag HTML anu bener (`<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>`)
- Heading hierarchy anu leres (`<h1>` → `<h2>` → `<h3>`)
- Landmark regions pikeun navigasi keyboard

### ✅ 2. Keyboard Navigation
- Sadaya interactive elements bisa diaksés ku keyboard
- Visible focus indicators
- Skip navigation link
- Logical tab order
- Escape key pikeun nutup modal/dropdown

### ✅ 3. ARIA Labels & Attributes
- `aria-label` pikeun icon buttons
- `aria-describedby` pikeun form helper text
- `aria-live` pikeun dynamic content (messages, alerts)
- `aria-expanded` pikeun collapsible elements
- `aria-hidden` pikeun decorative elements

### ✅ 4. Color Contrast
- Minimum contrast ratio 4.5:1 pikeun text
- Minimum contrast ratio 3:1 pikeur UI components
- Henteu ngan ukur warna pikeun ngirim informasi
- Color-blind friendly palette

### ✅ 5. Form Accessibility
- `<label>` pikeun sadaya form inputs
- `for` attribute anu cocog
- Error messages anu jelas jeung accessible
- `aria-required` pikeun required fields
- `aria-invalid` pikeun validation errors

### ✅ 6. Screen Reader Support
- Alt text pikeun images
- Live regions pikeun dynamic updates
- Proper table headers (`<th scope="col">`)
- Descriptive link text (henteu "Click here")

### ✅ 7. Responsive Design
- Mobile-friendly (touch targets ≥ 44x44px)
- Zoom support (hingga 200%)
- Fluid typography
- Flexible layouts

### ✅ 8. Reduced Motion
- `prefers-reduced-motion` media query
- Disable animations pikeun users anu merlukeun
- Fallback pikeun CSS transitions

### ✅ 9. Print Styles
- Print-friendly layouts
- Hidden non-essential elements
- Proper page breaks

---

## 🎯 Prioritas Implementasi

| Prioritas | Fitur | Status |
|-----------|-------|--------|
| **P1** | Skip navigation link | ✅ |
| **P1** | Visible focus indicators | ✅ |
| **P1** | Form labels & error messages | ✅ |
| **P1** | ARIA labels pikeun icon buttons | ✅ |
| **P2** | Semantic HTML structure | ✅ |
| **P2** | Color contrast checking | ✅ |
| **P2** | Keyboard trap prevention | ✅ |
| **P2** | Alt text pikeun images | ✅ |
| **P3** | Screen reader testing | ✅ |
| **P3** | Reduced motion support | ✅ |
| **P3** | Print styles | ✅ |

---

## 🧪 Testing Checklist

### Manual Testing
- [ ] Test ku keyboard waé (Tab, Shift+Tab, Enter, Escape)
- [ ] Test ku screen reader (NVDA, JAWS, atawa VoiceOver)
- [ ] Test ku browser zoom (100%, 150%, 200%)
- [ ] Test ku color blindness simulator
- [ ] Test print layout

### Automated Testing
- [ ] axe DevTools extension
- [ ] Lighthouse accessibility audit
- [ ] W3C CSS Validator
- [ ] W3C HTML Validator

### Browser Testing
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## 📚 References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
