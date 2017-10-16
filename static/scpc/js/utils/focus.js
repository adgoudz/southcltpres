
export default function focusBackground(container, backgroundWidth, backgroundHeight) {

    let update = (p, bgLength, containerLength, property, defaultPosition) => {
        if (bgLength > containerLength) {
            let ratio = bgLength / containerLength;
            let position = (p - 50) * ratio / (ratio - 1) + 50;
            container.css(property, `${position}%`);
        }
        else {
            container.css(property, defaultPosition);
        }
    };

    let focusX = container.data('focus-x');
    update(focusX, backgroundWidth, container.width(), 'background-position-x', '50%');

    let focusY = container.data('focus-y');
    update(focusY, backgroundHeight, container.height(), 'background-position-y', '50%');
}