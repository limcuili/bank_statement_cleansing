Why does my bank only provide bank statements as PDF?

Here I am having spent 3 hours as a python noob messily implementing a way to get my bank statements as a nice-enough CSV, where I can see the transactions. Attempting to analyse my year's finances is exactly how I've spent my Christmas day 2020.

Long story short, the goals were:
1. To keep it local to my machine - no one wants to upload their bank statements to an online parser.
2. To start from CSV as that's good practice for me as I'd like to improve my skills on data cleansing.
3. But most importantly... to see how much I've spent on Deliveroo this year.

If anyone is looking at this, it is worth noting the following:
- I did not want to use a PDF reading library, because that makes life too easy. So my input data is (ridiculously) to open each bank statement, ctrl+A, ctrl+C, and ctrl+V it into a CSV line. 
- Absolutely do not follow this as good practice. I manipulated data within dataframes and appended dataframes. This is horribly inefficient; you would want to manipulate the data as a list, where the final step is to convert it to a dataframe.

Cheers,
Merry Christmas & Happy Holidays.
