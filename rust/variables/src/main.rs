use std::io;


fn main() {
    let mut s = String::new();

    io::stdin().read_line(&mut s)
        .expect("Failed to read line");

    let word = first_word(&s);
    let first = &s[0..word];
    println!("{}", first);
}

fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}
