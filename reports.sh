#!/bin/bash
python3 analyzer.py > latest_report.txt
echo "Report generated: latest_report.txt"
echo "You can view the report using:"
echo "   cat latest_report.txt"
echo ""
#echo "To generate a detailed HTML report:"
#echo "   python3 reports.py"
#echo "This will create a detailed report in HTML format."
#echo "You can view the HTML report in your browser."
#echo "   open report.html"  # Adjust this command based on your OS
#echo ""
