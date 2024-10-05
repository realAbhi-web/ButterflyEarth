function toggleDisplay() {
    const writtenAnswer = document.getElementById('textBoxAnswer');
    const choiceAnswer = document.getElementById('multipleChoiceAnswer');
    i=Math.random()
    if (i< 0.5) {
        writtenAnswer.style.display = 'initial';
        choiceAnswer.style.display = 'none';
        // alert(i)
        // console.log("Displaying written answer form");
    } else {
        writtenAnswer.style.display = 'none';
        choiceAnswer.style.display = 'initial';
        // alert(i)
        // console.log("Displaying multiple choice form");
    }
}

window.onload = toggleDisplay;
