// sample Rust file for CodeQL pack tests
// we want to catch unwrap() and unsafe blocks

fn risky() {
    let x: Option<i32> = None;
    x.unwrap();
}

unsafe fn dangerous() {
    // do something unsafe
}
