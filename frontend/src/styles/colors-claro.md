# Paleta de Colores Claro Chile

Esta documentación define la paleta de colores oficial de Claro Chile aplicada al frontend del sistema VNM.

## Colores Principales de la Marca

### Rojo Claro (Principal)
- **Hex:** `#FF2315`
- **RGB:** `rgb(255, 35, 21)`
- **Uso:** Color principal de la marca, botones principales, elementos destacados
- **Variable CSS:** `--primary-color`

### Rojo Oscuro Claro  
- **Hex:** `#B52217`
- **RGB:** `rgb(181, 34, 23)`
- **Uso:** Hover states, variaciones del color principal
- **Variable CSS:** `--primary-dark`

### Rosa Coral Claro
- **Hex:** `#EEADA9`
- **RGB:** `rgb(238, 173, 169)`
- **Uso:** Elementos suaves, backgrounds de tarjetas especiales
- **Variable CSS:** `--primary-light`

## Colores Complementarios

### Azul Claro
- **Hex:** `#bbdff6`
- **RGB:** `rgb(187, 223, 246)`
- **Uso:** Elementos informativos, color secundario
- **Variable CSS:** `--secondary-color`, `--info-color`

### Rosa/Magenta
- **Hex:** `#ff007f`
- **RGB:** `rgb(255, 0, 127)`
- **Uso:** Elementos de acento, botones administrativos
- **Variable CSS:** `--accent-color`

### Lavanda Claro
- **Hex:** `#e6e6fa`
- **RGB:** `rgb(230, 230, 250)`
- **Uso:** Backgrounds suaves, elementos neutros
- **Variable CSS:** `--claro-light`

### Gris Claro
- **Hex:** `#e5e5e5`
- **RGB:** `rgb(229, 229, 229)`
- **Uso:** Bordes, separadores, elementos neutros
- **Variable CSS:** `--claro-neutral`

### Blanco
- **Hex:** `#ffffff`
- **RGB:** `rgb(255, 255, 255)`
- **Uso:** Fondos principales, texto en elementos oscuros
- **Variable CSS:** `--white`

## Gradientes Definidos

### Gradiente Principal
```css
background: linear-gradient(135deg, #FF2315 0%, #B52217 100%);
```
**Variable CSS:** `--primary-gradient`

### Gradiente Administrativo
```css
background: linear-gradient(135deg, #ff007f 0%, #FF2315 100%);
```

### Gradiente de Fondo
```css
background: linear-gradient(135deg, #ffffff 0%, #e6e6fa 100%);
```

### Gradiente de Tarjeta Admin
```css
background: linear-gradient(135deg, #EEADA9 0%, #bbdff6 100%);
```

## Aplicación en el Sistema

### Elementos de UI que usan la paleta:
- **Botones principales:** Rojo Claro (`#FF2315`)
- **Links y elementos interactivos:** Rojo Claro con hover a Rojo Oscuro
- **Badges y etiquetas:** Gradiente principal
- **Números estadísticos:** Rojo Claro
- **Fondo del dashboard:** Gradiente blanco a lavanda
- **Tarjetas administrativas:** Rosa coral a azul claro
- **Botones administrativos:** Rosa/magenta a rojo

### Estados de Interacción:
- **Hover:** Transición a `--primary-dark` (#B52217)
- **Focus:** Border en color principal con sombra suave
- **Active:** Mantenimiento del color principal con transform

## Consideraciones de Accesibilidad

- Todos los colores principales mantienen suficiente contraste con texto blanco
- Los colores complementarios se usan para elementos informativos no críticos
- Se mantienen los colores estándar para `success`, `warning` para consistencia

## Archivos Modificados

1. **`/frontend/src/styles/global.css`** - Variables CSS principales actualizadas
2. **`/frontend/src/pages/Dashboard.css`** - Estilos específicos del dashboard actualizados

## Fuente

Colores extraídos del sitio oficial de Claro Chile: https://www.clarochile.cl/
Referencia de marca oficial: https://brandfetch.com/clarochile.cl