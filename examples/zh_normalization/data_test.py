# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import re
from pathlib import Path

from text_normlization import TextNormalizer
from error_rate import char_errors


# delete english characters
# e.g. "你好aBC" -> "你 好"
def del_en_add_space(input: str):
    output = re.sub('[a-zA-Z]', '', input)
    output = [char + " " for char in output]
    output = "".join(output).strip()
    return output


def get_avg_cer(raw_dict, ref_dict, text_normalizer:TextNormalizer, output_dir):
    edit_distances = []
    ref_lens = []
    wf_ref = open(output_dir / "text.ref.clean", "w", encoding='utf-8')
    wf_tn = open(output_dir / "text.tn", "w", encoding='utf-8')
    for text_id in raw_dict:
        if text_id not in ref_dict:
            continue
        raw_text = raw_dict[text_id]
        gt_text = ref_dict[text_id]
        textnorm_text = text_normalizer.normalize_sentence(raw_text)

        gt_text = del_en_add_space(gt_text)
        textnorm_text = del_en_add_space(textnorm_text)
        wf_ref.write(gt_text + "(" + text_id + ")" + "\n")
        wf_tn.write(textnorm_text + "(" + text_id + ")" + "\n")

        # 计算编辑距离和字错率
        edit_distance, ref_len = char_errors(gt_text, textnorm_text)
        edit_distances.append(edit_distance)
        ref_lens.append(ref_len)

    return sum(edit_distances) / sum(ref_lens)


def main():
    parser = argparse.ArgumentParser(description="text normalization example.")
    parser.add_argument(
        "--input-dir",
        default="examples/zh_normalization/data",
        type=str,
        help="directory to preprocessed test data.")
    parser.add_argument(
        "--output-dir",
        default="examples/zh_normalization/output",
        type=str,
        help="directory to save textnorm results.")

    args = parser.parse_args()
    input_dir = Path(args.input_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    assert input_dir.is_dir()
    raw_dict, ref_dict = dict(), dict()
    raw_path = input_dir / "text"
    ref_path = input_dir / "text.ref"

    with open(raw_path, "r", encoding='utf-8') as rf:
        for line in rf:
            line = line.strip()
            line_list = line.split(" ")
            text_id, raw_text = line_list[0], " ".join(line_list[1:])
            raw_dict[text_id] = raw_text
    with open(ref_path, "r", encoding='utf-8') as rf:
        for line in rf:
            line = line.strip()
            line_list = line.split(" ")
            text_id, normed_text = line_list[0], " ".join(line_list[1:])
            ref_dict[text_id] = normed_text

    text_normalizer = TextNormalizer()

    avg_cer = get_avg_cer(raw_dict, ref_dict, text_normalizer, output_dir)
    print("The avg CER of text normalization is:", avg_cer)


def test_one():
    TN = TextNormalizer()

    text = '（中国）邮政17路'
    text_tn_1 = TN.normalize_sentence(text)
    print(text_tn_1)


if __name__ == "__main__":
    # 测试一条
    test_one()

    # main()