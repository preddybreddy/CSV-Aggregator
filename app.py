from flask import Flask, render_template, request, redirect, send_from_directory, url_for, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import util_functions
import io
import os

app = Flask(__name__)
app.config['ROOT_PATH'] = Path.cwd()
app.config['RAW_DATASETS'] = app.config['ROOT_PATH'] /'raw_datasets'
app.config['OUTPUT_DATASETS'] = app.config['ROOT_PATH'] / 'output_datasets'

@app.route('/', methods=['POST', 'GET'])
def upload_multiple():
    if request.method == 'POST':
        filenames = []
        files = request.files.getlist('multiple_files')
        for file in files:
            filename = secure_filename(file.filename)
            filenames.append(file.filename)
            try:
                file.save(str(app.config['RAW_DATASETS'] / Path(filename)))
            except FileNotFoundError:
                return 'Upload folder does not exist on server'
            except:
                return 'Error encountered in uploading file'
        d = {}
        for filename_i in range(len(filenames)):
            d['file'+ str(filename_i+1)] = filenames[filename_i]
        query_string = ''
        for key,value in d.items():    
            query_string += f'{key}={value}&'        
        return redirect(f'/process-csv?{query_string[0:len(query_string)-1]}&fileCount={len(d)}')
    else:
        return render_template('upload_multiple.html')


@app.route('/process-csv')
def data_processing():
    fileCount = request.args.get('fileCount', 0)
    filenames = [request.args.get(f'file{i + 1}') for i in range(int(fileCount))]
    df_cleaned = []
    for filename in filenames:
        df_cleaned.append(util_functions.load_and_clean_dataset(str(app.config['RAW_DATASETS'] / filename)))
    orig_columns = df_cleaned[0].columns
    df_aggregates = [util_functions.aggregated_ind_dataframes(df_cleaned[i]) for i in range(len(df_cleaned))]
    combined_df = util_functions.combined_df(df_aggregates)
    grp_by_control_probe = combined_df.groupby(combined_df.index)
    df_for_single_temperature_list = []
    for name, group in grp_by_control_probe:
        df_for_single_temperature_list.append(util_functions.output_dataframe_for_single_temperature(group.stack(),orig_columns, name ))

    final_df = util_functions.output_final_df(df_for_single_temperature_list)
    outputFileName = 'Aggregated Data' + '.xlsx'
    try:
        util_functions.output_file(outputFileName, final_df)
    except:
        return "Could not convert to excel"
    return_data = io.BytesIO()
    output_file_path = str(app.config['OUTPUT_DATASETS'] / outputFileName)
    with open(output_file_path, 'rb') as f:
        return_data.write(f.read())
    return_data.seek(0)
    os.remove(output_file_path)
    delete_raw_datasets()
    return send_file(return_data, mimetype='application/csv', as_attachment=True, download_name='Aggregated Data.xlsx')


def delete_raw_datasets():
    csv_files = os.listdir(app.config['RAW_DATASETS'])
    for f in csv_files:
        os.remove(app.config['RAW_DATASETS'] / f)
if __name__ == '__main__':
    app.run(debug=True)