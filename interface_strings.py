display_locale = "en_US.utf8"

return_code = {
    10: "    Unlocked    ",

    1: "Transaction Done",

    0: "OK",

    -1: "Unknown Error",

    -11: "Server Not\nAvailable",

    -21: "Unknon Card",
    -22: "Insufficent Bal.",
    -23: "Auth Required",
}

unlock = chr(7)+"    Unlock    "+chr(7)
terminal_locked_message = "Terminal Locked"
balance = "Balance: "
amount = "Amount: "
refill = "Refill: "
