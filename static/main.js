function bar(limit, elem){
    this.elem=elem;
    this.limit=limit;
}

function move(element) {
    var width = 1;
    var id = setInterval(frame, 10);
    var i = 0;
    function frame() {
        if (width >= element.limit) {
            clearInterval(id);
        } else {
            width++;
            element.elem.style.width = width + '%';
        }      
    }
}

function execute(){
    var elements = [new bar(75,document.getElementById("myBar1")),
    new bar(25,document.getElementById("myBar2")),
    new bar(50,document.getElementById("myBar3")),
    new bar(75,document.getElementById("myBar4")),
    new bar(75,document.getElementById("myBar5")),
    new bar(25,document.getElementById("myBar6")),
    new bar(25,document.getElementById("myBar7")),
    new bar(25,document.getElementById("myBar8")),
    new bar(50,document.getElementById("myBar9")),
    new bar(75,document.getElementById("myBar10"))];
    elements.forEach(element => {
        move(element);
    });
}

execute();