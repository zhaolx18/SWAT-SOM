# SWAT-SOM
SWAT-SOM (Soil and Water Assessment Tool— Self-Organizing Mapping Parameter Range Optimization Method)

### Code Language

- **Python:** 3.9.X
- **MATLAB:** R2021a

### Required Python Packages

- tkinter
- threading
- pandas
- numpy
- pyDOE2
- csv
- openopyxl

## Usage

### [`compile2.py` (User Interface)](compile2.py)

#### Test Case

The [`test_case`](test_case) folder includes example input and output files for the model.

> **Attention:** You need to specify the actual file locations in the following Python scripts (See Comments in scripts):
> - [`95PPU.py`](95PPU.py)
> - [`SOM-py.py`](SOM-py.py)
### Usage Steps 

#### 1. Latin Hypercube Sampling: `LHS.py`

- **Configuration File:** `Parameters.txt`
- **Runoff Measured Data:** `observed.txt`
- **Study Area Soil Type:** `soil.csv`
- **Original Model Parameter Files:** `RawModel` (The content from the SWAT `TxInOut` folder could be copied here. Examples could be seen in the `Rawmodel` within the `input` folder in the `test_case` directory.)
- **Output:** `results.csv/SOM.xlsx` will contain the sampling results and object functions. 

#### 2. Model Uncertainty Analysis: `95PPU.py`

- **Sampling Process File:** `MergedCSV_DataOnly.csv` (Sample at least 500 times for uncertainty analysis to calculate the model uncertainty (95PPU).)
- **Output:** The results are stored in `95PPU_result.txt`.

#### 3. SOM for Parameter Range Optimization

- **Configuration File:** `config-SOM.txt` (It reads the corresponding rows and columns from `data.xlsx` to perform calculations).
- **Output:** Select the best category from the output images and output it to the command line.
  - `SOM-results.xls`: Cluster result output file
  - `SOM-range.xls`: Parameter range optimization results

## License

This project is licensed under the [GPLv3] - see the [LICENSE](LICENSE) for details.

## Contact

Lixin Zhao - [zlx22@mails.jlu.edu.cn](mailto:zlx22@mails.jlu.edu.cn)

## Acknowledgments

- **[[Hongyan Li](https://teachers.jlu.edu.cn/LHY29/zh_CN/index.htm)/[Changhai Li](https://github.com/IchinoseHimeki)]**: For their invaluable insights and expertise in developing the core algorithm that significantly enhanced the performance of our model. Their innovative approaches to problem-solving and tireless dedication to research excellence greatly influenced the success of our project.