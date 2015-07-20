if (!localStorage.getItem('no-hiring')) {
    console.log("                                                                                                                            ,---. ");
    console.log(",--.   ,--.,------.,--.,------. ,------.    ,--.  ,--. ,-----. ,--------.    ,--.  ,--.,--.,------. ,--.,--.  ,--. ,----.   |   | ");
    console.log("|  |   |  ||  .---'|  ||  .--. '|  .---'    |  ,'.|  |'  .-.  ''--.  .--'    |  '--'  ||  ||  .--. '|  ||  ,'.|  |'  .-./   |  .' ");
    console.log("|  |.'.|  ||  `--, `-' |  '--'.'|  `--,     |  |' '  ||  | |  |   |  |       |  .--.  ||  ||  '--'.'|  ||  |' '  ||  | .---.|  |  ");
    console.log("|   ,'.   ||  `---.    |  |\\  \\ |  `---.    |  | `   |'  '-'  '   |  |       |  |  |  ||  ||  |\\  \\ |  ||  | `   |'  '--'  |`--'  ");
    console.log("'--'   '--'`------'    `--' '--'`------'    `--'  `--' `-----'    `--'       `--'  `--'`--'`--' '--'`--'`--'  `--' `------' .--.  ");
    console.log("                                                                                                                            '--'  ");
    console.log("But everone else gets to 'hide' job adverts in their source code, so this is what it might look like if we were desperate enough");
    console.log("to hire anyone who's figured out how to press Ctrl-Shift-I* on their keybord.  That said, the ascii font we're using is awful - if");
    console.log("you want to do some pro-bono work finding a better one, shoot us an email!");
    console.log("(Type 'noHiring()' into the console to never have to see this message again)");
    console.log('');
    console.log('* Not guaranteed to be a universal shortcut.');
}

function noHiring() {
    localStorage.setItem('no-hiring', 'aww...');
}
