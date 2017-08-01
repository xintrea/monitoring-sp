CREATE TABLE measureValue(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          valueName TEXT,
          valueData TEXT,
          timeStamp TEXT
        );

CREATE TABLE situation(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          valueName TEXT,
          ruleName TEXT,
          timeStamp TEXT
        );
